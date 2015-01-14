function onReady() {
    var sel_method = $('#sel_method');
    sel_method.change(function() {
        var sel_method_param = $('.sel_method_param');
        if (sel_method.val() == "turnee") {
            sel_method_param.show();
        } else {
            sel_method_param.hide();
        }
    });


}
$(document).ready(onReady);