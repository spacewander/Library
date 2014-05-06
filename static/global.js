var debugMode = true;

// log the message when in debug mode
function log(message) {
    if (!debugMode) {
        return;
    }
    if (console) {
        console.log(message);
    }
}

// store the value with key
function store(key, value) {
    if (!value) {
      console.warn('should be a value stored by ' + key);
    }
    else {
        try {
            console.log(key);
            localStorage.setItem(key, encodeURIComponent(value));
            log('store: ' + value);
        }
        catch (e) {
            log('store: ' + value + ' failed.');
        }
    }
}

// get the value with key
function get(key) {
    if (!key) {
        console.warn('should have a key to get something');
    }
    else {
        var value = localStorage.getItem(key);
        try {
            return value ? decodeURIComponent(value) : '';
        }
        catch (e) {
            return '';
        }
    }
}

// 简单json处理
function obj2json(o) {
    if (!o) {
        return "";
    }
    return JSON.stringify(o);
}
function json2obj(s) {
    try {
        if (s) {
            return JSON.parse(s);
        } 
        else {
            return {};
        }
    }
    catch (e) {
        return {};
    }
}

var baseURL = window.location.href.replace(/(\?|#).*$/,"").replace(/((http:|https|)\/.*\/)(.*$)/, "$1");

function getURLComponent() {
    return window.location.href.replace(/(\?|#).*$/, "").replace(/^.*\//, "");
}

// defines some URL patterns
var Global = {
    homepage : baseURL,
    showEntries : baseURL + 'entries',
    adminEntries : baseURL + 'admin',
    login : baseURL + 'login'
};


