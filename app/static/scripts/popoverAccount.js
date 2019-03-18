$(document).ready(function(){
    $('[data-toggle="popover"]').popover({
        placement : 'bottom',
        html : true,
        content :   '<div class="media">' +
                        '<div class="media-body">' +
                            '<h4 class="media-heading">Jhon Carter</h4>' +
                            '<p>Excellent Bootstrap popover! I really love it.</p>' +
                        '</div>' +
                    '</div>'
    });

    $(document).on("click", ".popover .close" , function(){
        $(this).parents(".popover").popover('hide');
    });

    $('.popover-dismiss').popover({
        trigger: 'focus'
    })

});