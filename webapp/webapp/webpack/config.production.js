/* eslint-disable */
const webpack = require('webpack');
const OptimizeCssAssetsPlugin = require('optimize-css-assets-webpack-plugin');

const makeConfig = require('./config.base');


// In production, append hash to filenames
const filenameTemplate = 'webapp/[name]-[hash]';

const config = makeConfig({
    filenameTemplate: filenameTemplate,

    mode: 'production',

    devtool: 'source-map',

    namedModules: false,
    minimize: true,

    publicPath: process.env.DJANGO_STATIC_URL || '/assets/',

    prependSources: [],

    plugins: [
        // Minimize CSS
        new OptimizeCssAssetsPlugin({
            cssProcessorPluginOptions: {
                preset: ['default', {discardComments: {removeAll: true}}],
            },
        }),
    ],

    performance: {
        hints: 'warning',
    },
});
console.log("Using PRODUCTION config");
console.log(`DJANGO_STATIC_URL=${process.env.DJANGO_STATIC_URL}`);

module.exports = config;
