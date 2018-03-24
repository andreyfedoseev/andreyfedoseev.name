const path = require('path');
// const CleanWebpackPlugin = require('clean-webpack-plugin');
const LiveReloadPlugin = require('webpack-livereload-plugin');

module.exports = {
  entry: {
    "index.js": "index.js"
  },
  output: {
    filename: '[name]',
    path: path.resolve(__dirname, 'theme/static/dist')
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
  plugins: [
    new LiveReloadPlugin()
  ],
  devServer: {
    contentBase: './theme/dist'
  },
  resolve: {
    modules: [
      "theme/static",
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
