let webpack = require('webpack');
let path = require('path');
let glob = require('glob');
let ExtractTextPlugin = require("extract-text-webpack-plugin");
let CleanWebpackPlugin = require('clean-webpack-plugin');
let BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  entry: {
    app: [
      './src/main.js',
      './src/main.scss'
    ],
    vendor: ['jquery', 'bootstrap', 'popper.js'],
  },
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'js/[name].[chunkhash].js',
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
    new CleanWebpackPlugin('dist'),
    new BundleTracker({filename: './webpack-stats.json'}),
  ]
};