let webpack = require('webpack');
let merge = require('webpack-merge');
var path = require('path');
var glob = require('glob');
let UglifyJSPlugin = require('uglifyjs-webpack-plugin');
let PurifyCSSPlugin = require('purifycss-webpack');
let CleanWebpackPlugin = require('clean-webpack-plugin');
let common = require('./webpack.common.js');

module.exports = merge(common, {
  output: {
    path: path.resolve(__dirname, 'assets'),
    filename: 'js/[name].[chunkhash].js',
  },
  plugins: [
    new UglifyJSPlugin(),
    new CleanWebpackPlugin('assets'),
    new webpack.LoaderOptionsPlugin({
        minimize: true,
      }),
    new PurifyCSSPlugin({
        // Give paths to parse for rules. These should be absolute!
        paths: glob.sync(path.join(__dirname, '/templates/*.html')),
        minimize: true
      })
   ]
});