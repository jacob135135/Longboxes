# -*- coding: utf-8 -*-


def index():
    #This checks if user is logged in (using a session variable storing user's id)
    #If user is not logged in, they are redirected to login webpage
    #session.current_user_id = None    -> this logs out
    if session.current_user_id is None:
        redirect('login.html')

    #Data to show list of users with links to their collections
    users_data = db(db.users.id >0).select()

    public_boxes = db(db.boxes.is_public == 'True').select(db.boxes.id)
    count = db.box_contents.box_id.count()

    #5 biggest public boxes
    box_ids = db(db.box_contents.box_id.belongs(public_boxes)).select(db.box_contents.box_id,
                                                               groupby=db.box_contents.box_id, orderby=~count, limitby=(0,5))
    #5 newest public boxes
    box_ids2 = db(db.boxes.is_public == 'True').select(db.boxes.id, orderby=~db.boxes.date_created, limitby=(0,5))

    ids = []
    for id in box_ids:
        ids.append(id.box_id)

    for id in box_ids2:
        ids.append(id.id)

    boxes_data = [] #All boxes and their data (Need to to it this way as otherwise they might be out of order)
    for box_id in ids:
        boxes_data.append(db(db.boxes.id == box_id).select().first()) #All data for current box

    comic_basic_data = None
    boxes_info = []
    comics_info = []
    boxes_lengths = []

    for user_box in boxes_data:
        date_cr = user_box.date_created.strftime("%d%b%Y") # Date format (e.g.  07Nov2015)
        usern = db(db.users.id == user_box.owner_id).select(db.users.username).first()['username']

        boxes_info.append({'id': user_box.id, 'title': user_box.title, 'date_created':date_cr, 'owner_id': user_box.owner_id, 'owner_usern': usern})
        comics_ids = db(db.box_contents.box_id == user_box.id).select(db.box_contents.comic_id)

        boxes_lengths.append(len(comics_ids)) #Need to know how many comics in each box
        for id in comics_ids:
            com_id = id.comic_id
            comics_info.append(db(db.comics.id == com_id).select())

    return dict(users_data = users_data, comics_data = comics_info, boxes_info = boxes_info, boxes_lengths = boxes_lengths)


def logout():
    session.current_user_id = None
    return dict()


#When this webpage is visited 1st time, user is given a form to fill. Once the form is submitted details are correct, user will be logged in
def login():
    login_form=FORM(DIV(LABEL('Username: *', _for='username'), _class="col-sm-2 control-label"),
                   DIV(INPUT(_name='username', requires=IS_NOT_EMPTY(), _class="form-control"), _class="col-sm-10"),
                   DIV(LABEL('Password: *', _for='publisher'), _class="col-sm-2 control-label"),
                   DIV(INPUT(_name='password',_type='password', requires=IS_NOT_EMPTY(), _class="form-control"), _class="col-sm-10"),
                   DIV('* Required field.'),
                   DIV(INPUT(_type='submit', _id='submit_btn', _class="form-control btn btn-primary")), _class="form-horizontal")

    #After submitting form, username and password should be available - if it is a valid combination, user will be logged in and redirected to index
    if (request.vars.username and request.vars.password):
        user_details = db((db.users.username == request.vars.username) & (db.users.password == request.vars.password)).select()
        try:
            session.current_user_id = user_details[0].id
            redirect('viewUserComics.html')
        except IndexError:
            session.current_user_id = None

    #If the form is filled in and username/password is incorrect, user will not be logged in and redirected to index but warned instead
    if login_form.accepts(request,session):
        response.flash = 'Incorrect username or password, please try again'

    elif login_form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'

    return dict(login_form=login_form, args = session.current_user_id)


def addUser():
    add_user_form=FORM(DIV(LABEL('Username: *', _for='username'), _class="col-sm-2 control-label"),
                   DIV(INPUT(_name='username', requires=IS_NOT_EMPTY(), _class="form-control"), _class="col-sm-10"),
                   DIV(LABEL('Password: *', _for='password'), _class="col-sm-2 control-label"),
                   DIV(INPUT(_name='password',_type='password', requires=IS_NOT_EMPTY(), _class="form-control"), _class="col-sm-10"),
                      DIV('* Required field.'),
                   DIV(INPUT(_type='submit', _id='submit_btn', _class="form-control btn btn-primary")), _class="form-horizontal")


    #Check if username is used
    if add_user_form.accepts(request,session):
        user_details = db(db.users.username == request.vars.username).select()

    #If username not already in use, out of index exception would occur, this needs to be prevented
        try:
            user_id = user_details[0].id
            response.flash = 'Username already in use, please choose a different username'
        except IndexError:
            #Add user to db, log them in and redirect to home page
            user_id = db.users.insert(username=request.vars.username,password=request.vars.password)
            #Create Unfiled box for the new user
            db.boxes.insert(owner_id=user_id, title='Unfiled', is_public = False)
            session.current_user_id = user_id
            redirect('index.html')

    elif add_user_form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'

    return dict(add_user_form=add_user_form, args = session.current_user_id)


def addComic():
    #Make sure user is logged in
    if session.current_user_id is None:
        redirect('login.html')

    boxes=db(db.boxes.owner_id==session.current_user_id).select() # this gives us all boxes belonging to the user

    addform = FORM(DIV(LABEL('Box to put in: *', _for='title'), _class="col-sm-2 control-label"),
           DIV(SELECT(_name='selected_box', *[OPTION(boxes[i].title, _value=str(boxes[i].id)) for i in range(len(boxes))], _class="form-control"),
               _class="col-sm-10"),
           DIV(LABEL('Comic image:', _for='image'), _class="col-sm-2 control-label"),
           DIV(INPUT(_name='image', _type='file', requires = IS_EMPTY_OR(IS_IMAGE(maxsize=(400, 300),
               error_message='Maximum size is 400 x 300. You can add or change picture later.')), _class="help-block"), _class="col-sm-10"),
           DIV(LABEL('Comic Name: *', _for='title'), _class="col-sm-2 control-label"),
           DIV(INPUT(_name='title', _placeholder="Name of comic, example: Batman", requires=IS_NOT_EMPTY(),
               _class="form-control"), _class="col-sm-10"),
           DIV(LABEL('Publisher: *', _for='publisher'), _class="col-sm-2 control-label"),
           DIV(INPUT(_name='publisher', _placeholder="Publisher name, example: Carlsen Comics",requires=IS_NOT_EMPTY(),
               _class="form-control"), _class="col-sm-10"),
           DIV(LABEL('Issue number: *', _for='issue_number'), _class="col-sm-2 control-label"),
           DIV(INPUT(_name='issue_number', _id='issue_number', _placeholder="Issue number, example: 415",requires = IS_INT_IN_RANGE(0, 1000000,
               error_message='Must be a positive number'), _class="form-control"), _class="col-sm-10"),
           DIV(LABEL('Writers: *', _for='writers'), _class="col-sm-2 control-label"),
           DIV(INPUT(_name='writers', _placeholder="Names separated by comma, example: Jack Kay, Peter Tan, Ivan Tay",
               requires=IS_NOT_EMPTY(),_class="form-control"), _class="col-sm-10"),
           DIV(LABEL('Artists: *', _for='artists'), _class="col-sm-2 control-label"),
           DIV(INPUT(_name='artists', _placeholder="Names separated by comma, example: Jack Kay, Peter Tan, Ivan Tay",
               requires=IS_NOT_EMPTY(), _class="form-control"), _class="col-sm-10"),
           DIV(LABEL('Short description (max 300 words), currently: 0 *', _id='short_descr_count', _for='short_description'),
               _class="col-sm-2 control-label"), #jQuery will make sure text is max 300 words
           DIV(TEXTAREA(_name='short_description', _id='short_descr', _placeholder="Short description, example: Batman is a superhero...",
               requires=IS_NOT_EMPTY(), _class="form-control"), _class="col-sm-10"),
           DIV('* Compulsory fields.'),
           DIV(INPUT(_type='submit', _id='submit_btn', _class="form-control btn btn-primary")), _class="form-horizontal",
               _onchange="updateShortDescr();", _onkeydown="updateShortDescr();")

    #@IAPT On acceptance we are going to add the item to the database.
    if addform.accepts(request,session):
        comic_id = db.comics.insert(title=request.vars.title,publisher=request.vars.publisher, issue_number=request.vars.issue_number,
                                       short_description=request.vars.short_description, image=request.vars.image)
        db.commit

        __add_authors(comic_id)

        #Finally we add comic to the box user specified
        db.box_contents.insert(box_id=request.vars.selected_box, comic_id=comic_id)
        response.flash = 'Comic successfully added to your collection.'

    else:
        response.flash = 'Please complete the form below to add a new comic.'

    return dict(add_comic_form=addform)


def addBox():
    #Make sure user is logged in
    if session.current_user_id is None:
        redirect('login.html')
    #@IAPT Form containing all of the fields in DIVs to allow for block layout
    addform = FORM(DIV(LABEL('Box Name: *', _for='title'), _class="col-sm-2 control-label"),
                   DIV(INPUT(_name='title', _id='box_title', _placeholder="Name of box to create, example: Action", requires=IS_NOT_EMPTY(),
                       _class="form-control"), _class="col-sm-10"),
                   DIV(LABEL('Visibility *', _for='visibility'), _class="col-sm-2 control-label"),
                   DIV(SELECT('Private','Public', value='b',_name='visibility', _class="form-control"), _class="col-sm-10"),
                      DIV('* Compulsory fields.'),
                   DIV(INPUT(_type='submit', _id='submit_btn', _class="form-control btn btn-primary")), _class="form-horizontal",
                         _onchange="dontAllowUnfiledName()")

    #@IAPT On acceptance we are going to add the item to the database.
    if addform.accepts(request,session):
        if (request.vars.visibility == 'Private'):
            is_publ = False
        else:
            is_publ = True

        db.boxes.insert(title=request.vars.title,is_public=is_publ, owner_id=session.current_user_id)
        response.flash = 'New box successfully created.'
    elif addform.errors:
        response.flash = 'One or more of your form fields has an error. Please see below for more information'
    else:
        response.flash = 'Please complete the form below to add a new box.'
    return dict(add_box_form=addform)


def viewUserComics():
    #Make sure user is logged in
    if session.current_user_id is None:
        redirect('login.html')

    #User can be redirected here after deleting a comic or box-> need to display success message
    if request.get_vars.deleted_comic is not None:
        response.flash = 'Comic successfully removed from the box'
    elif request.get_vars.deleted_box is not None:
        comics_moved = request.get_vars.comics_moved
        response.flash = "Box successfully removed. " + comics_moved + " comic(s) moved to Unfiled box."
    if request.get_vars.user_id is not None:
        user_id = request.get_vars.user_id
    else:
        user_id = session.current_user_id

    boxes_data = db(db.boxes.owner_id == user_id).select()

    comic_basic_data = None
    boxes_info = []
    comics_info = []
    boxes_lengths = []

    for user_box in boxes_data:
        date_cr = user_box.date_created.strftime("%d%b%Y") # Date format (e.g.  07Nov2015)
        if (user_box.is_public):
            privacy = 'Public'
        else:
            privacy = 'Private'

        #Need image, title, issue number, owner username -> (front end work: onclick redirect to page which gives full info based on comic_id)
        if ((session.current_user_id == user_id) or (privacy == 'Public')): #If does not belong to owner, show only public boxes
            boxes_info.append({'id': user_box.id, 'title': user_box.title, 'privacy': privacy, 'date_created':date_cr})
            comics_ids = db(db.box_contents.box_id == user_box.id).select(db.box_contents.comic_id)

            boxes_lengths.append(len(comics_ids)) #Need to know how many comics in each box
            for id in comics_ids:
                com_id = id.comic_id
                comics_info.append(db(db.comics.id == com_id).select())

    owner_data = db(db.users.id == user_id).select() #User's password and username (needed if the viewer is not the owner)
    return dict(comics_data = comics_info, boxes_info = boxes_info, boxes_lengths = boxes_lengths, owner_data = owner_data)

def viewComicFullInfo():
    #Make sure user is logged in
    if session.current_user_id is None:
        redirect('login.html')

    comic_id = request.get_vars.id
    comic_data = db(db.comics.id == comic_id).select()
    comic_authors = db(db.comic_authors.comic_id == comic_id).select(db.comic_authors.author_id)

    author_ids = [] #This will be a list of author_ids (e.g. [12, 13, 121, 43])
    for author in comic_authors:
        author_ids.append(author.author_id)

    comic_writers = db((db.authors.type == 'WRITER') & (db.authors.id.belongs(author_ids))).select()
    comic_artists = db((db.authors.type == 'ARTIST') & (db.authors.id.belongs(author_ids))).select()

    boxes=db(db.boxes.owner_id==session.current_user_id).select() #This gives all boxes belonging to the user

    #Form to put comic to another box
    add_form = FORM(DIV(LABEL('Put this comic into another box:', _for='title'), _class="col-sm-4 control-label"),
           DIV(SELECT(_name='selected_box', *[OPTION(boxes[i].title, _value=str(boxes[i].id)) for i in range(len(boxes))], _class="form-control"),
               _class="col-sm-4"),
           DIV(INPUT(_type='submit', _id='submit_btn', _class="btn btn-primary")), _class="form-horizontal bordered")

    if add_form.accepts(request,session):
        if (request.get_vars.owner == 'True'):
            #If the user is the owner - only add link to the comic (no need to duplicate comic)
            db.box_contents.insert(box_id=request.vars.selected_box,comic_id=request.get_vars.id)
            response.flash = 'Comic successfully added to the box'
        else:
            #Need to copy the comic and add it to user's selected box
            comic = db(db.comics.id == request.get_vars.id).select(db.comics.ALL).first()
            new_comic_id = db.comics.insert(**db.comics._filter_fields(comic))
            db.box_contents.insert(box_id=request.vars.selected_box,comic_id=new_comic_id)
            #Need to add links to authors into comic_authors table
            authors_ids = db(db.comic_authors.comic_id == comic_id).select(db.comic_authors.author_id)
            for author in authors_ids:
                db.comic_authors.insert(comic_id=new_comic_id,author_id=author.author_id)

            response.flash = 'You have successfully added the comic to your collection'

    #Not that much data sent here - more about splitting it into smaller groups
    return dict(comic_data = comic_data[0], comic_writers = comic_writers, comic_artists = comic_artists, res = comic_authors, add_form =add_form)


def editBox():
    #Make sure user is logged in
    if session.current_user_id is None:
        redirect('login.html')

    box_id = request.get_vars.id
    if box_id is not None:
        box_data = db(db.boxes.id == box_id).select().first()
        box_title = box_data.title
        box_public_val = "Private"
        if box_data.is_public:
            box_public_val = "Public"

        editform = FORM(DIV(LABEL('Box Name: *', _for='title'), _class="col-sm-2 control-label"),
                        DIV(INPUT(_name='title', _id='box_title', _placeholder="Name of box", _value=box_title, requires=IS_NOT_EMPTY(),
                                  _class="form-control"), _class="col-sm-10"),
                        DIV(LABEL('Visibility *', _for='visibility'), _class="col-sm-2 control-label"),
                        DIV(SELECT('Private','Public', value=box_public_val,_name='visibility', _class="form-control"), _class="col-sm-10"),
                        DIV('* Compulsory fields.'),
                        DIV(INPUT(_type='submit', _id='submit_btn', _class="form-control btn btn-primary")), _class="form-horizontal",
                        _onchange="dontAllowUnfiledName()", _onkeydown="dontAllowUnfiledName()")

        if editform.accepts(request,session):
            if (request.vars.visibility == 'Private'):
                is_publ = False
            else:
                is_publ = True

            #Update record in db
            box_data.update_record(title=request.vars.title,is_public=is_publ)
            redirect(URL("editBox.html?success=True&id=" + box_id), client_side=True)
        elif editform.errors:
            response.flash = 'One or more of your form fields has an error. Please see below for more information'
        elif request.get_vars.success: #User can be redirected here after editing a comic -> need to display success message
            response.flash = 'Box successfully updated'
        else:
            response.flash = 'Use the form below to update box information.'
        return dict(edit_box_form=editform)


def editComic():
    #Make sure user is logged in
    if session.current_user_id is None:
        redirect('login.html')

    comic_id = request.get_vars.id
    if comic_id is not None:
        comic_data = db(db.comics.id == comic_id).select().first()
        comic_title = comic_data.title
        comic_image = comic_data.image
        comic_issue_number = comic_data.issue_number
        comic_publisher = comic_data.publisher
        comic_short_description = comic_data.short_description

        comic_authors = db(db.comic_authors.comic_id == comic_id).select(db.comic_authors.author_id)
        author_ids = [] #This will be a list of author_ids (e.g. [12, 13, 121, 43])
        for author in comic_authors:
            author_ids.append(author.author_id)

        comic_writers = db((db.authors.type == 'WRITER') & (db.authors.id.belongs(author_ids))).select()
        comic_artists = db((db.authors.type == 'ARTIST') & (db.authors.id.belongs(author_ids))).select()

        #Need to give user a comma separated string of authors
        writers = ""
        incl_comma = False
        for writer in comic_writers:
            if incl_comma:
                writers +=  ", "
            writers += writer.full_name
            incl_comma = True

        artists = ""
        incl_comma = False
        for artist in comic_artists:
            if incl_comma:
                artists +=  ", "
            artists += artist.full_name
            incl_comma = True

        edit_form = FORM(DIV(LABEL('Comic Name: *', _for='title'), _class="col-sm-2 control-label"),
           DIV(INPUT(_name='title', _placeholder="Name of comic, example: Batman", _value=comic_title, requires=IS_NOT_EMPTY(),
               _class="form-control"), _class="col-sm-10"),
           DIV(LABEL('Update image:**', _for='image'), _class="col-sm-2 control-label"),
           DIV(INPUT(_name='image', _type='file', requires = IS_EMPTY_OR(IS_IMAGE(maxsize=(400, 300),
               error_message='Maximum size is 400 x 300.')), _class="help-block"), _class="col-sm-10"),
           DIV(LABEL('Publisher: *', _for='publisher'), _class="col-sm-2 control-label"),
           DIV(INPUT(_name='publisher', _placeholder="Publisher name, example: Carlsen Comics", _value=comic_publisher ,requires=IS_NOT_EMPTY(),
               _class="form-control"), _class="col-sm-10"),
           DIV(LABEL('Issue number: *', _for='issue_number'), _class="col-sm-2 control-label"),
           DIV(INPUT(_name='issue_number', _id='issue_number', _value=comic_issue_number, _placeholder="Issue number, example: 415",
               requires = IS_INT_IN_RANGE(0, 1000000,
               error_message='Must be a positive number'), _class="form-control"), _class="col-sm-10"),
           DIV(LABEL('Writers: *', _for='writers'), _class="col-sm-2 control-label"),
           DIV(INPUT(_name='writers', _value=writers, _placeholder="Names separated by comma, example: Jack Kay, Peter Tan, Ivan Tay",
               requires=IS_NOT_EMPTY(),_class="form-control"), _class="col-sm-10"),
           DIV(LABEL('Artists: *', _for='artists'), _class="col-sm-2 control-label"),
           DIV(INPUT(_name='artists', _value=artists, _placeholder="Names separated by comma, example: Jack Kay, Peter Tan, Ivan Tay",
               requires=IS_NOT_EMPTY(), _class="form-control"), _class="col-sm-10"),
           DIV(LABEL('Short description (max 300 words), currently: 0 *', _id='short_descr_count', _for='short_description'),
               _class="col-sm-2 control-label"), #jQuery will make sure text is max 300 words
           DIV(TEXTAREA(_name='short_description', _id='short_descr', _value=comic_short_description,
               _placeholder="Short description, example: Batman is a superhero...", requires=IS_NOT_EMPTY(), _class="form-control"),
               _class="col-sm-10"),
           DIV('* Compulsory fields.'),
           DIV('** Current image remains active unless new image selected. I.e. not choosing a file does NOT delete current image'),
           DIV(INPUT(_type='submit', _id='submit_btn', _class="form-control btn btn-primary")), _class="form-horizontal",
               _onchange="updateShortDescr();", _onkeydown="updateShortDescr();")


        if edit_form.accepts(request,session):
            #Update record in db (apart from authors)
            comic_data.update_record(title=request.vars.title,publisher=request.vars.publisher,issue_number=request.vars.issue_number,
                                    short_description=request.vars.short_description)

            #Check if image uploaded, if exception raised => image uploaded
            try:
                len(request.vars.image) #This means image not uploaded
            except TypeError:
                comic_data.update_record(image=request.vars.image) #Image has been uploaded (as the exception occured); update image in db

            #To update authors, firstly remove old links for them and then parse them and recreate as in add_comic
            db(db.comic_authors.comic_id == comic_id).delete()
            __add_authors(comic_id)
            db.commit

            redirect(URL("editComic.html?success=True&id=" + comic_id), client_side=True)
        elif edit_form.errors:
            response.flash = 'One or more of your form fields has an error. Please see below for more information'

        #User can be redirected here after editing a comic -> need to display success message
        elif request.get_vars.success:
            response.flash = 'Comic successfully updated'
        else:
            response.flash = 'Use the form below to update comic information.'

    return dict(edit_form=edit_form)


def deleteBox():
    #Make sure user is logged in
    if session.current_user_id is None:
        redirect('login.html')

    box_id = request.get_vars.id
    box_comics_raw = db(db.box_contents.box_id == box_id).select(db.box_contents.comic_id)
    comic_ids = [] #This will be ids of all comics in box to be deleted
    for comic in box_comics_raw:
        comic_ids.append(comic.comic_id)

    comics_moved = 0;
    user_unfiled_box = db((db.boxes.owner_id == session.current_user_id) & (db.boxes.title == 'Unfiled')).select()
    user_unfilled_box_id = user_unfiled_box[0].id
    #Check if comic is NOT in other boxes - if that is the case, need to link the comic into Unfiled box
    for comic_id in comic_ids:
        if (db(db.box_contents.comic_id == comic_id).count() < 2):
            db.box_contents.insert(box_id=user_unfilled_box_id,comic_id=comic_id)
            comics_moved += 1

    #Once the links to comics not present in other boxes are added, the box and all its contents need to be deleted
    db(db.boxes.id == box_id).delete()
    db(db.box_contents.id == box_id).delete()

    redirect(URL("viewUserComics.html?deleted_box=True&comics_moved=" + str(comics_moved)))
    return dict(raw_data = box_comics_raw)


def deleteComic():
    #Make sure user is logged in
    if session.current_user_id is None:
        redirect('login.html')

    comic_id = request.get_vars.comic_id
    box_id = request.get_vars.box_id

    #Remove box_id - comic_id link (no effect on box or comic)
    db((db.box_contents.box_id == box_id) & (db.box_contents.comic_id == comic_id)).delete()
    redirect(URL("viewUserComics.html?deleted_comic=True"))
    return dict()


def search():
    #Make sure user is logged in
    if session.current_user_id is None:
        redirect('login.html')

    query = request.get_vars.query
    #Ids of boxes to limit search to (currently logged-in user's boxes + public boxes)
    avail_box_ids = db((db.boxes.is_public == 'True') | (db.boxes.owner_id == session.current_user_id)).select(db.boxes.id)

    ## GIVE RESULTS BY TYPE (results by title, publisher, writer and artist)

    #Ids of comics by title
    matching_title = db(db.comics.title.contains(query)).select(db.comics.id)
    comic_title_ids = db(db.box_contents.box_id.belongs(avail_box_ids) & db.box_contents.comic_id.belongs(matching_title)).select()

    #Ids of comics by publisher
    matching_publ = db(db.comics.publisher.contains(query)).select(db.comics.id)
    comic_publ_ids = db(db.box_contents.box_id.belongs(avail_box_ids) & db.box_contents.comic_id.belongs(matching_publ)).select()

    #Ids of comics by writer
    matching_writer_ids = db((db.authors.full_name.contains(query)) & (db.authors.type == 'WRITER')).select(db.authors.id)
    matching_writer = db(db.comic_authors.author_id.belongs(matching_writer_ids)).select(db.comic_authors.comic_id)

    comic_ids_list = []
    for com_id in matching_writer:
        comic_ids_list.append(com_id.comic_id)

    comic_writer_ids = db(db.box_contents.box_id.belongs(avail_box_ids) & (db.box_contents.comic_id.belongs(comic_ids_list))).select()

    #Ids of comics by artist
    matching_artist_ids = db((db.authors.full_name.contains(query)) & (db.authors.type == 'ARTIST')).select(db.authors.id)
    matching_artist = db(db.comic_authors.author_id.belongs(matching_artist_ids)).select(db.comic_authors.comic_id)

    comic_ids_list = []
    for com_id in matching_artist:
        comic_ids_list.append(com_id.comic_id)
    comic_artist_ids = db(db.box_contents.box_id.belongs(avail_box_ids) & db.box_contents.comic_id.belongs(comic_ids_list)).select()

    lengths = []
    ids = []
    cur_length = 0
    for id in comic_title_ids:
        ids.append(id.comic_id)
        cur_length += 1
    lengths.append(cur_length)

    for id in comic_publ_ids:
        ids.append(id.comic_id)
        cur_length += 1
    lengths.append(cur_length)

    for id in comic_writer_ids:
        ids.append(id.comic_id)
        cur_length += 1
    lengths.append(cur_length)

    for id in comic_artist_ids:
        ids.append(id.comic_id)
        cur_length += 1
    lengths.append(cur_length)

    stuff = []
    comic_authors = []
    comics_info = []
    owner_data = []

    for id in ids:
        comics_info.append(db(db.comics.id == id).select())
        comic_box_id = db(db.box_contents.comic_id == id).select(db.box_contents.box_id).first()
        try: #In case there was problem with data, should not break if user is not known
            comic_owner_id = db(db.boxes.id == comic_box_id.box_id).select(db.boxes.owner_id).first()
            comic_owner_username = db(db.users.id == comic_owner_id.owner_id).select(db.users.username).first()
            owner_data.append([comic_owner_id.owner_id, comic_owner_username.username])
        except AttributeError:
            pass

    return dict(comics_data=comics_info, categ_lengths = lengths, owner_data=owner_data, total_comics=cur_length)

def __add_authors(comic_id):
    #Need to get array of writers and artists from the form
    writers = [x.strip() for x in request.vars.writers.split(',')] #Splits by "'" and trims the string
    artists = [x.strip() for x in request.vars.artists.split(',')] # e.g. " what, is , this?  " => ['what', 'is', 'this?']
    WRITER_TYPE = 'WRITER'
    ARTIST_TYPE = 'ARTIST'

    #Comic added to db, now we need to create entries for authors (writers and artists), firstly we check if there is not an entry already
    #If entry in db, we get its id and link it with the comic id in comic_authors table
    for cur_name in writers:
        if (len(cur_name) > 1):
            entry = db((db.authors.full_name == cur_name) & (db.authors.type == WRITER_TYPE)).select()
            try:
                cur_writ_id= entry[0].id
            except IndexError:
                #Author does not exist, add new entry for them
                cur_writ_id = db.authors.insert(full_name = cur_name, type = WRITER_TYPE)
                #Add (comic_id,author_id) into comic_authors table
            db.comic_authors.insert(comic_id = comic_id, author_id = cur_writ_id)

    #Now do the same with artists
    for cur_name in artists:
        if (len(cur_name) > 1):
            entry = db((db.authors.full_name == cur_name) & (db.authors.type == ARTIST_TYPE)).select()
            try:
                cur_writ_id= entry[0].id
            except IndexError:
                #Author does not exist, add new entry for them
                cur_writ_id = db.authors.insert(full_name = cur_name, type = ARTIST_TYPE)
                #Add (comic_id,author_id) into comic_authors table
            db.comic_authors.insert(comic_id = comic_id, author_id = cur_writ_id)


# DO NOT DELETE -> THIS ALLOWS SEEING IMAGE ON THE PAGE
def download():
    return response.download(request, db)
