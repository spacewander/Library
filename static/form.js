var Form = {};

// show error message
Form.showError = function() {
    $('.form-error').show();
};
// hide error message
Form.hideError = function() {
    $('.form-error').hide();
};
// add the error report element to the appreciate input tag
//
// @param [String] error 
//      the error message
Form.addError = function (error) {
         
};

// this code is copied from the docs of jQuery 
// to make the effect of val() on textarea normal
$.valHooks.textarea = {
  get: function( elem ) {
    return elem.value.replace( /\r?\n/g, "\r\n" );
  }
};

// remember the input of add entry form after each submit
Form.rememberEntry = function() {
    $('form.add_entry').submit(function(event) {
        store('title', $('input[name=title]').val());
        store('category', $('input[name=category]').val());
        store('buydate', $('input[name=buydate]').val());
        store('introduction', $('textarea[name=introduction]').val());
        //event.preventDefault();
    });
};

// set the value of add entry form back if there is empty.
Form.recallEntry = function() {
    form_input_names = [ 'title', 'category', 'buydate'];
    for (var name in form_input_names) {
        if ($('form.add_entry > input[name=' + name + ']').val()) {
            continue;
        }
        var value = get(name);
        if (value) {
            $('input[name=' + name + ']').val(value);
            store(name, '');
        }
    }
    if (!$('form.add_entry > textarea[name=introduction]').val()) {
        var textarea_value = get('introduction');
        if (textarea_value) {
            $('textarea[name=introduction]').val(textarea_value);
            store('introduction', '');
        }
    }
};

// remember the input of login form after each submit
Form.rememberLogin = function() {
    $('form#login').submit(function(event) {
        store('username', $('input[name=username]').val());
    });
};

// set the value of login form back if there is empty.
Form.recallLogin = function() {
    if (!$('form#login > input[name=username]').val()) {
        var username = get('username');
        if (username) {
            $('input[name=login]').val(username);
            store('username', '');
        }
    }
};

// check if the title input is valid. If not, show the error message out
Form.checkTitle = function() {
    
};

// check if the category input is valid. If not, show the error message out
Form.checkCategory = function() {
    
};

// check if the buydate input is valid. If not, show the error message out
Form.checkBuydate = function() {
    
};

// check if the username input is valid. If not, show the error message out
Form.checkUsername = function() {
    
};

// check if the password input is valid. If not, show the error message out
Form.checkPassword = function() {
    
};

$(document).ready( function() {
    if (!Global) {
        return;
    }
    // if the current page is home page
    if ( window.location.href === Global.adminEntries ) {
        Form.addError();
        Form.recallEntry();
        Form.checkTitle();
        Form.checkCategory();
        Form.checkBuydate();
        Form.rememberEntry();
    }
    // should the login page
    else if ( window.location.href === Global.login ) {
        Form.addError();
        Form.recallLogin();
        Form.checkUsername();
        Form.checkPassword();
    }
});


