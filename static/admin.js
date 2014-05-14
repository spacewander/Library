var Admin = {};

// show Add Entry widget
Admin.addEntry = function() {
    $('label[for=add_entry]').click(function () {
        $('form.add_entry').show();
        $('form.edit_entry').hide();
    });
};

// hide Add Entry widget and show Edit Entry widget
Admin.editEntry = function() {
    $('span.edit').click(function () {
        $('form.add_entry').hide();
        $('form.edit_entry').show();

        // a tricky way to get the value to edit
        var editData = $(this).siblings('div.none-style');
        var title = editData.children('div[data-type=title]').text();
        var category = editData.children('div[data-type=category]').text();
        var buydate = editData.children('div[data-type=buydate]').text();
        var introduction = editData.children('div[data-type=introduction]').text();

        $('form.edit_entry input[name=title]').val(title);
        $('form.edit_entry input[name=category]').val(category);
        $('form.edit_entry input[name=buydate]').val(buydate);
        $('form.edit_entry textarea[name=introduction]').text(introduction);

        $('form.edit_entry').submit(function () {
            $(this).hide();
        });
    });
};

$(document).ready( function() {
    if (!Global) {
        return;
    }
    // if the current page is home page
    if ( window.location.href === Global.adminEntries ||
        window.location.href === Global.homepage ) {
        Admin.addEntry();
        Admin.editEntry();
    }
});

