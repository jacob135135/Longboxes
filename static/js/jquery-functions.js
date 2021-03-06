/**
    Updates Short description text in add comic to reflect current number of words
**/
function updateShortDescr() 
{
    txt = $('#short_descr').val();
    if (txt == '') 
	{
		word_count = 0;
    } else 
	{
        word_count = txt.replace( /[^\w ]/g, "" ).split( /\s+/ ).length; //http://stackoverflow.com/questions/9864644/jquery-character-and-word-count
    }

    $('#short_descr_count').text ("Short description (max 300 words), currently: " + word_count + " *");
    
    if (word_count > 300)
	{
		$('#submit_btn').prop('disabled', true);
    } else 
	{
		$('input[type="submit"]').prop('disabled', false);
    }
}

function dontAllowUnfiledName() 
{
    cur_val = $('#box_title').val();
    
    if (cur_val == 'Unfiled') 
	{
		$('#submit_btn').prop('disabled', true);
    } else 
	{
		$('input[type="submit"]').prop('disabled', false);
    }
}

function deleteBox(box_id) 
{
	ask=confirm("Are you sure you want to delete this box? \n Comics contained in this box only will be moved to Unfiled box");
    if(ask) 
	{
		window.location="deleteBox?id=" + box_id;
	}
}


function deleteComic(box_id, comic_id) 
{
	ask=confirm("Are you sure you want to remove this comic from this box? \n (This comic will NOT be removed from other boxes automatically)");
    if(ask) 
	{
		window.location="deleteComic?box_id=" + box_id + "&comic_id=" + comic_id;
	}
}


function populateShortDescr() 
{
	$('#short_descr').val($('#short_descr').attr('value'))
}

function doSearch()
{
	searched = $('#search_input').val();
	window.location="search?query=" + searched;
}


