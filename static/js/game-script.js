$(function() {
    $('#talk').click(function () {
        $('#talk-select').show();
        $('#buy-select').hide();
        $('#food-select').hide();
        $('#food-button').hide();
         $('#buy-button').hide();
    });
    $('#buy').click(function () {
        $('#talk-select').hide();
        $('#buy-select').show();
        $('#food-select').hide();
        $('#food-button').hide();
        $('#buy-button').hide();
    });
    $('#feed').click(function () {
        $('#talk-select').hide();
        $('#buy-select').hide();
        $('#food-select').show();
        $('#food-button').hide();
        $('#buy-button').hide();
    });
    $('.food-option').click(function () {
        $('#food-button').show();
    })
     $('.buy-option').click(function () {
        $('#buy-button').show();
    })
    $('.talk-option').click(function () {
        $('#talk-button').show();
    })
    $('#tutorial-delete').click(function () {
        $('.tutorial-box').hide();
    })
    $('#tutorial').click(function () {
        $('.tutorial-box').show();
    })
});