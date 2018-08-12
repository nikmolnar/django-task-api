import path from 'path'
import UglifyJsPlugin from 'uglifyjs-webpack-plugin'

export default {
    mode: 'production',
    devtool: 'source-map',
    entry: './src/index.js',
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: path.resolve(__dirname, 'node_modules'),
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['env']
                    }
                }
            }
        ]
    },
    output: {
        filename: 'django-task-api.js',
        path: path.resolve(__dirname, 'dist')
    },
    resolve: {
        modules: [
            path.resolve(__dirname, 'node_modules')
        ]
    },
    optimization: {
        minimizer: [
            new UglifyJsPlugin({})
        ]
    }
}
