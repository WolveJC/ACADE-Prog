const path = require("path");
const webpack = require("webpack");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const CopyWebpackPlugin = require("copy-webpack-plugin");

// Lee Wolves-Page/.env en local. En Vercel, BACKEND_URL se configura
// como variable de entorno del proyecto (Project Settings) y ya llega
// aquí en process.env sin necesidad de este archivo.
require("dotenv").config();

module.exports = {
  mode: process.env.NODE_ENV || "development",
  entry: "./src/index.js",
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "bundle.[contenthash].js",
    clean: true,
    publicPath: "/",
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/, // React y JS moderno
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/preset-env", "@babel/preset-react"],
          },
        },
      },
      {
        test: /\.css$/i, // Tailwind + PostCSS
        use: ["style-loader", "css-loader", "postcss-loader"],
      },
      {
        test: /\.(png|jpe?g|gif|svg|webp)$/i, // imágenes (incluye webp)
        type: "asset/resource",
      },
      {
        test: /pdf\.worker\.min\.mjs$/, // worker de PDF.js
        type: "asset/resource",
      },
    ],
  },
  resolve: {
    extensions: [".js", ".jsx"],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: "./public/index.html",
      favicon: "./public/favicon.ico",
    }),
    // Inyecta la URL del backend como una constante fija en el bundle
    // (webpack reemplaza process.env.BACKEND_URL por este string literal
    // en tiempo de build -- no es una variable real en el navegador).
    // Con esto, RecipeCard.jsx / TriviaWidget.jsx / CafePage.jsx pueden
    // leer process.env.BACKEND_URL sin que el bundle quede roto.
    new webpack.DefinePlugin({
      "process.env.BACKEND_URL": JSON.stringify(
        process.env.BACKEND_URL || "http://localhost:5000"
      ),
    }),
    // Antes solo HtmlWebpackPlugin tocaba public/ (y solo copiaba
    // index.html + favicon.ico). Todo lo demás que vive suelto en
    // public/ (docs/doc_proj.pdf, manifest.json, robots.txt,
    // sitemap.xml, logos, etc.) nunca llegaba a dist/, aunque
    // `npm start` lo serviera bien gracias a devServer.static.
    // Este plugin copia el resto de public/ tal cual, para que
    // `npm run build` quede equivalente a lo que ya veías en dev.
    new CopyWebpackPlugin({
      patterns: [
        {
          from: "public",
          to: ".",
          globOptions: {
            // Evita duplicar/pisar lo que HtmlWebpackPlugin ya genera.
            ignore: ["**/index.html", "**/favicon.ico"],
          },
          noErrorOnMissing: true,
        },
      ],
    }),
  ],
  devServer: {
    static: path.resolve(__dirname, "public"),
    hot: true,
    port: 3000,
    historyApiFallback: true,
    allowedHosts: "all",
  },
};
