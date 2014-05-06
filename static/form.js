var Form = {};

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

Form.rememberEntry = function() {
    $('form.add_entry').submit(function(event) {
        store('title', $('input[name=title]').val());
        store('category', $('input[name=category]').val());
        store('buydate', $('input[name=buydate]').val());
        store('introduction', $('textarea[name=introduction]').val());
        //event.preventDefault();
    });
};

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

Form.rememberLogin = function() {
    
};

Form.recallLogin = function() {
  
};

Form.checkTitle = function() {
    
};

Form.checkCategory = function() {
    
};

Form.checkBuydate = function() {
    
};

Form.checkUsername = function() {
    
};

Form.checkPassword = function() {
    
};

$(document).ready( function() {
    console.log(Global);
    if (!Global) {
        return;
    }
    // if the current page is home page
    if ( window.location.href === Global.adminEntries ) {
        Form.checkTitle();
        Form.checkCategory();
        Form.checkBuydate();
        Form.recallEntry();
        Form.rememberEntry();
    }
    // should the login page
    else if ( window.location.href === Global.login ) {
        Form.recallLogin();
        Form.checkUsername();
        Form.checkPassword();
    }
});

