function onReady() {
    var sel_method = $('#sel_method');
    sel_method.change(function() {
        this.form.submit();
    });

    $('#cross_method').change(function() {
        this.form.submit();
    });
}
$(document).ready(onReady);