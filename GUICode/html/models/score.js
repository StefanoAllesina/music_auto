var mongoose = require('mongoose');

var scoreSchema = mongoose.Schema({
    name: String,
    pages: [String]
});

module.exports = mongoose.model('score', scoreSchema);