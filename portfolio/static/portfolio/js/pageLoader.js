$(document).ready(function () {
    // On start of page, cover the screen with a pre page loader
    $('body').css('overflow-y', 'hidden');
    setTimeout(
        function () {
            $('.page-loader').css('display', 'none');
            $('body').css('overflow-y', 'auto');
        }, 1000);
});