let webpack = require('webpack');
let path = require('path');
let glob = require('glob');
let ExtractTextPlugin = require("extract-text-webpack-plugin");
let BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  entry: {
    app: [
      './resources/main.js',
      './resources/main.scss'
    ],
    vendor: ['jquery', 'bootstrap', 'popper.js'],
  },

  module: {
    rules: [
      {
        test: /\.s[ac]ss$/,
        use: ExtractTextPlugin.extract({
          use: ['css-loader', 'sass-loader'],
          fallback: 'style-loader',
        })
      },
      {
        test: /\.(svg|eot|ttf|woff|woff2)$/,
        use: 'file-loader'
      },
      {
        test: /\.(png|jpg|gif)$/,
        loaders: [
          {        
            loader: 'file-loader',
            options: {
              name: 'images/[name].[hash].[ext]'
            }
          },
          'img-loader',
        ]
      },
      {
        test: /\.js$/, 
        exclude: /node_modules/, 
        loader: 'babel-loader'
      },
    ],
  },

  plugins: [
    new ExtractTextPlugin('[name].[hash].css'),
    new BundleTracker({filename: './webpack-stats.json'}),
  ]
};