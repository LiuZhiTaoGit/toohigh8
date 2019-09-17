$(function () {
   $(".info ").click(function () {
     //alert("已选中");
       $(".form1").show();
   });
    $('.ih-item').click(function () {
        $('.form1').hide();
    });
    $("#data-sub").click(function () {
        $.ajax({
            type:"post",

        })
    });
    $('.counter-value').each(function(){
        $(this).prop('Counter',0).animate({
            Counter: $(this).text()
        },{
            duration: 3500,
            easing: 'swing',
            step: function (now){
                $(this).text(Math.ceil(now));
            }
        });
    });
})
