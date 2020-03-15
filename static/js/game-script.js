$(function() {
    $('#talk').click(function () {//talkボタンが押されると、talk-selectを表示、
                                    // 他のselectリストを非表示
        $('#talk-select').show();
        $('#buy-select').hide();
        $('#food-select').hide();
        $('.submit-button').hide();
    });
    $('#buy').click(function () {
        $('#talk-select').hide();
        $('#buy-select').show();
        $('#food-select').hide();
        $('.submit-button').hide();
    });
    $('#feed').click(function () {
        $('#talk-select').hide();
        $('#buy-select').hide();
        $('#food-select').show();
        $('.submit-button').hide();
    });
    $('.food-option').click(function () {//food-optionが押されると、確定ボタンを表示
        $('#food-button').show();
    });
     $('.buy-option').click(function () {
        $('#buy-button').show();
    });
    $('.talk-option').click(function () {
        $('#talk-button').show();
    });
    $('#tutorial-delete').click(function () {//チュートリアル内のバツボタンが押されると、チュートリアルを消す
        $('.tutorial-box').hide();
    });
    $('#tutorial').click(function () {///チュートリアルボタンが押されると、チュートリアルを表示
        $('.tutorial-box').show();
    });
    $('.action-cancel').click(function () {//select-listの一番下の「やめておく」が押されると、selectlistを非表示
        $('.select-list').hide();
        $('.submit-button').hide();
    });
});