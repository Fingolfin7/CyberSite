$(document).ready(function(){
    $("#logo").on('change', function(){
        var input = $('#logo');
        var img_preview = $(`#preview`);
        console.log(img_preview);
        img_preview.empty();

        if($(input)[0].files){
            for(var i = 0; i < $(input)[0].files.length; i++){
              var img_src = URL.createObjectURL($(input)[0].files[i]);
              URL.revokeObjectURL($(input)[0].files[i]); // free up memory
              var img_name = $(input)[0].files[i].name;

              img_preview.append(`<img src="${img_src}" alt="${img_name}"
              style="border: 2px solid lightgrey; margin-left: auto; margin-right: auto; display: block;"
              />`);
            }
        }
        else{
            console.log(`Nope! ${$(input)[0].files}`);
        }
    });
});
