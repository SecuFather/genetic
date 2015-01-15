function onReady() {

    $('.selectpicker').change(function() {
        this.form.submit();
    });
}
$(document).ready(onReady);