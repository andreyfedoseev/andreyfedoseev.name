const path = require('path');

module.exports = {
  entry: {
    "index.js": "index.js"
  },
  output: {
    filename: '[name]',
    path:'/dist'
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        exclude: /project\/static/,
        use: [
          'style-loader',
          {
            loader: "css-loader",
            options: {
              modules: false
            }
          }
        ]
      },
      {
        test: /\.scss$/,
        use: [
          'style-loader',
          {
            loader: "css-loader",
            options: {
              modules: false
            }
          },
          {
            loader: "sass-loader" // compiles Sass to CSS
          }
        ]
      }
    ]
  },
  devServer: {
    contentBase: '/dist'
  },
  resolve: {
    modules: [
      "/static",
      "node_modules",
    ]
  },
  resolveLoader: {
    modules: [
      "node_modules"
    ]
  },
  devtool: 'source-map'
};
