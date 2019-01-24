import fetch from 'isomorphic-fetch'
import Cookie from 'js-cookie'

export const options = {
    baseURL: '/tasks/',
    csrfCookieName: 'csrftoken',
    csrfHeaderName: 'X-CSRF-Token',
    corsMode: 'same-origin',
    pollInterval: 1000  // Time to wait, in seconds, between polls
}

export const run = (task, inputs, progressCallback = null, callback = null, errback = null) => {
    const promise = new Promise((resolve, reject) => {
        createTask(task, inputs).then(json => {
            pollUntilDone(json.uuid, progressCallback).then(json => {
                if (json.status === 'succeeded') {
                    if (callback !== null) {
                        callback(json)
                    }
                    resolve(json)
                }
                else {
                    if (errback !== null) {
                        errback(json)
                    }
                    reject(json)
                }
            })
        }).catch(err => {
            if (errback !== null) {
                errback(err)
            }
            reject(err)
        })
    })
    return promise
}

const createTask = (task, inputs) => {
    let { baseURL, corsMode, csrfCookieName, csrfHeaderName } = options
    const data = {
        task,
        inputs
    }
    const headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json'
    }
    headers[csrfHeaderName] = Cookie.get(csrfCookieName)

    return fetch(baseURL, {
        method: 'POST',
        mode: corsMode,
        cache: 'no-cache',
        headers,
        redirect: 'follow',
        referrer: window.location,
        credentials: corsMode === 'cors' ? 'include' : 'same-origin',
        body: JSON.stringify(data)
    }).then(raiseForStatus).then(response => response.json())
}

const pollUntilDone = (uuid, progressCallback = null) => {
    let { baseURL, corsMode, pollInterval } = options

    return new Promise((resolve, reject) => {
        const poll = () => {
            return fetch(`${baseURL}${uuid}/`, {
                mode: corsMode,
                cache: 'no-cache',
                headers: {
                    'Accept': 'application/json'
                },
                redirect: 'follow',
                referrer: window.location,
                credentials: corsMode === 'cors' ? 'include' : 'same-origin'
            })
                .then(raiseForStatus)
                .then(response => response.json())
                .then(json => {
                    if (progressCallback !== null) {
                        progressCallback(json)
                    }

                    if (json.status === 'pending' || json.status === 'running') {
                        setTimeout(() => poll(), pollInterval)
                    }
                    else {
                        resolve(json)
                    }
                })
                .catch(err => reject(err))
        }
        poll()
    })
}

const raiseForStatus = response => {
    if (response.status < 200 || response.status > 299) {
        throw new Error(`Bad status: ${response.status}`)
    }
    return response

}
