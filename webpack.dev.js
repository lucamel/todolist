let CleanWebpackPlugin = require('clean-webpack-plugin');
var path = require('path');
let merge = require('webpack-merge');
let common = require('./webpack.common.js');

module.exports = merge(common, {
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: 'js/[name].[chunkhash].js',
      },
    devtool: 'inline-source-map',

    plugins: [
        new CleanWebpackPlugin('dist'),
    ]
});