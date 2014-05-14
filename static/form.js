var Form = {};

// stop the default event (for example, store the event triggle by submit)
function stopDefaultEvent() {
    event.preventDefault();
}

// disable submit event
//
// @param [String] form
//      the selector of form
Form.hideSubmit = function(form) {
    $(form).on('submit', stopDefaultEvent);
};

// enable submit event
//
// @param [String] form
//      the selector of form
Form.showSubmit = function(form) {
    $(form).off('submit', stopDefaultEvent);
};

// show error message
//
// @param [String] elem
//      the input which should show the error
// @param [String] error
//      the error message
Form.showError = function(elem, error) {
    if (!error || !elem) {
        return;
    }
    $(elem).siblings('.form-error').text(error);
    $(elem).siblings('.form-error').css('visibility', 'visible');
};

// hide error message
//
// @param [String] elem
//      the input which should show the error
Form.hideError = function( elem ) {
    if (!elem) {
        return;
    }
    $('.form-error').css('visibility', 'hidden');
};

// add the error report element to the appreciate input tag
Form.addError = function () {
    $('form.add_entry input[type=text]').each(function () {
        $(this).after('<span class="form-error">输入框内输入不正确</span>');
    });
    $('form.edit_entry input[type=text]').each(function () {
        $(this).after('<span class="form-error">输入框内输入不正确</span>');
    });
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
        if ($('form.add_entry input[name=' + name + ']').val()) {
            continue;
        }
        var value = get(name);
        if (value) {
            $('input[name=' + name + ']').val(value);
            store(name, '');
        }
    }
    if (!$('form.add_entry textarea[name=introduction]').val()) {
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
    $('form.add_entry input[name=title]').blur( function() {
        if ($(this).val().match(/^\s*$/) ) {
            Form.showError(this, '标题不能为空!');
        }
        else {
            Form.hideError(this);
        }
    });
    $('form.edit_entry input[name=title]').blur( function() {
        if ($(this).val().match(/^\s*$/) ) {
            Form.showError(this, '标题不能为空!');
        }
        else {
            Form.hideError(this);
        }
    });
};

// check if the category input is valid. If not, show the error message out
Form.checkCategory = function() {
    $('form.add_entry input[name=category]').blur( function() {
        if ($(this).val().match(/^\s*$/) ) {
            Form.showError(this, '分类不能为空!');
        }
        else if ($(this).val().match(/[\d!@#$%^&*()+-]/) ) {
            Form.showError(this, '不能包括特殊字符，比如!@#$%^&*()+-和数字');
        }
        else {
            Form.hideError(this);
        }
    });
    $('form.edit_entry input[name=category]').blur( function() {
        if ($(this).val().match(/^\s*$/) ) {
            Form.showError(this, '分类不能为空!');
        }
        else if ($(this).val().match(/[\d!@#$%^&*()+-]/) ) {
            Form.showError(this, '不能包括特殊字符，比如!@#$%^&*()+-和数字');
        }
        else {
            Form.hideError(this);
        }
    });
};

// check if the buydate input is valid. If not, show the error message out
Form.checkBuydate = function() {
    $('form.add_entry input[name=buydate]').blur( function() {
        if ($(this).val().match(/^\s*$/) ) {
            Form.showError(this, '购买日期不能为空!');
        }
        else if (!$(this).val().match(/\d\d\d\d-\d*\d-\d*\d/) ) {
            Form.showError(this, '购买日期格式错误，应该为yyyy-mm-dd');
        }
        else {
            Form.hideError(this);
        }
    });
    $('form.edit_entry input[name=buydate]').blur( function() {
        if ($(this).val().match(/^\s*$/) ) {
            Form.showError(this, '购买日期不能为空!');
        }
        else if (!$(this).val().match(/\d\d\d\d-\d*\d-\d*\d/) ) {
            Form.showError(this, '购买日期格式错误，应该为yyyy-mm-dd');
        }
        else {
            Form.hideError(this);
        }
    });
};

// check if the username input is valid. Called after typing
Form.checkUsername = function() {
    $('form#login input[name=username]').blur( function() {
        // if the input is empty and the password is not empty.
        // This will happen when a user delete his/her username by mistake.
        if ($(this).val().match(/^\s*$/) &&
            $(this).parents('form#login')
                   .find('input[name=password]').val() !== '') {
            // we can not use animate with background-color with basuc jQuery
            //$(this).animate({'background-color' : 'red'}, 1000);
            // 有点傻气的闪烁动画
            var bgcolor = $(this).css('background-color');
            setTimeout(function () {
                $('form#login input[name=username]').css('background-color', 'red');
            }, 50);
            setTimeout(function () {
                $('form#login input[name=username]').css('background-color', bgcolor);
            }, 200);
            setTimeout(function () {
                $('form#login input[name=username]').css('background-color', 'red');
            }, 500);
            setTimeout(function () {
                $('form#login input[name=username]').css('background-color', bgcolor);
            }, 800);
            $('form#login input[name=username]').css('background-color', bgcolor);
        }
    });
};

// check if the password input is valid. Called after typing
Form.checkPassword = function() {
    $('form#login input[name=password]').blur( function() {
        // if the input is empty and the username is not empty
        // This will happen when a user forgets to input his/her password
        if ($(this).val().match(/^\s*$/) &&
            $(this).parents('form#login')
                   .find('input[name=username]').val() !== '') {
            var bgcolor = $(this).css('background-color');
            setTimeout(function () {
                $('form#login input[name=password]').css('background-color', 'red');
            }, 50);
            setTimeout(function () {
                $('form#login input[name=password]').css('background-color', bgcolor);
            }, 200);
            setTimeout(function () {
                $('form#login input[name=password]').css('background-color', 'red');
            }, 500);
            setTimeout(function () {
                $('form#login input[name=password]').css('background-color', bgcolor);
            }, 800);
            $('form#login input[name=password]').css('background-color', bgcolor);
        }
    });
};

// check if the inputs of login page are valid. Called before submit
Form.checkLogin = function() {
    $('form#login input[type=submit]').click( function () {
        var shouldHideSubmit = false;
        $('form#login input[type=text]').each( function() {
            if ($(this).val().match(/^\s*$/) ) {
                shouldHideSubmit = true;
            }
        });

        if (shouldHideSubmit) {
            $('form#login input[type=text]').each( function() {
                (function (that, bgcolor) {
                    setTimeout(function () {
                        $(that).css('background-color', 'red');
                    }, 50);
                    setTimeout(function () {
                        $(that).css('background-color', bgcolor);
                    }, 200);
                    setTimeout(function () {
                        $(that).css('background-color', 'red');
                    }, 500);
                    setTimeout(function () {
                        $(that).css('background-color', bgcolor);
                    }, 800);
                }) (this, $(this).css('background-color') );
            });
            Form.hideSubmit('form#login');
        }
        else {
            Form.showSubmit('form#login');
        }

    });
};

$(document).ready( function() {
    if (!Global) {
        return;
    }
    // if the current page is home page
    if ( window.location.href === Global.adminEntries ||
        window.location.href === Global.homepage ||
        window.location.href === Global.showEntries) {

        Form.addError();
        Form.recallEntry();
        Form.checkTitle();
        Form.checkCategory();
        Form.checkBuydate();
        Form.rememberEntry();
    }
    // else should the login page
    else if ( window.location.href === Global.login ) {
        Form.recallLogin();
        Form.checkUsername();
        Form.checkPassword();
        Form.checkLogin();
    }
});

