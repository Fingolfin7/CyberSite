function add_poc_image(input){
        var input_parent = input.closest('.poc_label');
        var cell_top = input.closest('.poc_cell_top');
        //console.log(img_preview);
        //img_preview.empty();

        if($(input)[0].files){
            for(var i = 0; i < $(input)[0].files.length; i++){
              var img_src = URL.createObjectURL($(input)[0].files[i]);
              URL.revokeObjectURL($(input)[0].files[i]); // free up memory
              var img_name = $(input)[0].files[i].name;

              cell_top.append(`<img src="${img_src}" alt="${img_name}" class="poc_img">`);
            }
            input_parent.hide();
        }
        else{
            console.log(`Nope! ${$(input)[0].files}`);
        }
    }
