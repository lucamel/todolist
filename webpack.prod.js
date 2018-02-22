let webpack = require('webpack');
let merge = require('webpack-merge');
var path = require('path');
var glob = require('glob');
let UglifyJSPlugin = require('uglifyjs-webpack-plugin');
let PurifyCSSPlugin = require('purifycss-webpack');
let common = require('./webpack.common.js');

module.exports = merge(common, {
    plugins: [
    new UglifyJSPlugin(),
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