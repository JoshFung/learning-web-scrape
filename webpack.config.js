const path = require('path');

module.exports = {
    entry: ["./client/src/App.tsx", "./api/app.js"],
    output: {
        filename: './bundle.js'
    },
    resolve: {
        modules: ['node_modules'],
        extensions: ['.ts', '.tsx', '.js', '.jsx',]
    },
}