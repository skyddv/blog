/**
 * Created by comyn on 16-10-29.
 */
var path = require('path');
var webpack = require('webpack');

module.exports = {
    entry: [
        'react-hot-loader/patch',
        'webpack-dev-server/client?http://127.0.0.1:3000',
        'webpack/hot/dev-server',
        './app/index'
    ],
    output: {
        path: path.join(__dirname, 'dist'),
        filename: 'bundle.js',
        publicPath: '/assets/'
    },
    plugins: [
        new webpack.HotModuleReplacementPlugin()
    ],
    module: {
        loaders: [
            {
                test: /\.js$/,
                loader: 'babel',
                exclude: /node_modules/,
                include: path.join(__dirname, 'app')
            },
            {
                test: /\.sass$/,
                loaders: ['style', 'css', 'sass']
            },
            {
                test: /\.(jpe?g|gif|png|svg)$/i,
                loaders: ['file']
            },
            {
                test: /\.css$/,
                loaders: 'style'
            }
        ]
    }
};
