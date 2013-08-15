if (jQuery != undefined) {
    var django = {
        'jQuery':jQuery,
    }
}
(function($, document) {
    $(document).ready(function() {

        $('.geocomplete-widget').each(function(){
            $('.geocomplete', $(this)).geocomplete({
                map: '#'+$('.geocomplete-map', $(this)).attr('id'),
                location: "San Francisco, CA",
                details: $(this).closest('form')
            });

        });



    });

})(django.jQuery, document);
