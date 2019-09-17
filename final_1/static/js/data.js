function a() {
    var num=0;
    var t = setInterval(function(){
        num++;
        $('.span1').innerText=num;
        if(num==10){
            clearInterval(t);
        }
    },100);
}
