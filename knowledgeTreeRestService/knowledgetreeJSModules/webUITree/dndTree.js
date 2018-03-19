function close_modal() {
    $(document).foundation('reveal', 'close');
}

var tree_root;
var connect_node_modal_active = false;
var node_to_connect = null;
var view_node_modal_active = false;
var node_to_view = null;
var create_node_modal_active = false;
var rename_node_modal_active = false;
var move_node_modal_active = false;
var copy_node_modal_active = false;
var create_node_parent = null;
var node_to_rename = null;
var node_to_move_copy = null;
var node_to_copy = null;
var allNodes = [];

var with_relation = "subject-with-relation";
var subject_work_or_person = "subject";
var currentValue = "subject";

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function getIp() {
    return getParameterByName('userip')
}
// var url = "http://127.0.0.1:5000/knowledgeTree/api/v1.0/";
var url = "http://" + getIp() + ":5000/knowledgeTree/api/v1.0/";

function getauth() {
    // hidden form will have a fld where we will store string version of passed query string
    auth = getParameterByName('name') + ":" + getParameterByName('psw');
    return auth;
}

function connect_nodes() {
    if (currentValue == "Subject" || currentValue == "Work") connect_subject_work_nodes();
    else connect_person_work_nodes();
}

function connect_subject_work_nodes() {
    subject = $('#ConnectSubjectNode').val();
    work = $('#ConnectWorkNode1').val();
    node_relation = $('#ConnectNodeRelation1').val();
    console.log('Connected Subject:' + subject + " to Work:" + work + " with relation:" + node_relation);

    d3.xhr(url + "subject-to-work")
        .header("Content-Type", "application/json")
        .header("Authorization", "Basic " + btoa(auth))
        .post(
            JSON.stringify({
                "subject": subject,
                "work": work,
                "relation": node_relation
            }),
            function(err, rawdata) {
                if (err) console.log("error:", err)
                else {
                    try {
                        // var data = JSON.parse(str_replace(chr(13), str_replace(chr(10), rawdata)));
                        console.log("response:", rawdata.response, "status:", rawdata.status);
                    } catch (error) { console.log("error:", err, "response:", rawdata) };
                }
            }
        );
    close_modal();
}

function connect_person_work_nodes() {
    person = $('#ConnectPersonNode').val();
    work = $('#ConnectWorkNode2').val();
    node_relation = $('#ConnectNodeRelation2').val();
    console.log('Connected Person:' + person + " to Work:" + work + " with relation:" + node_relation);

    d3.xhr(url + "person-to-work")
        .header("Content-Type", "application/json")
        .header("Authorization", "Basic " + btoa(auth))
        .post(
            JSON.stringify({
                "person": person,
                "work": work,
                "relation": node_relation
            }),
            function(err, rawdata) {
                if (err) console.log("error:", err)
                else {
                    try {
                        // var data = JSON.parse(str_replace(chr(13), str_replace(chr(10), rawdata)));
                        console.log("response:", rawdata.response, "status:", rawdata.status);
                    } catch (error) { console.log("error:", err, "response:", rawdata) };
                }
            }
        );
    close_modal();
}

function showNodeConnectTree(d) {
    // if (subjects_works_or_persons_list == "works")
    if (currentValue == "Subject") {
        keyword = "&subject=";
        page = "subject_work.html";
    } else if (currentValue == "Work") {
        keyword = "&work=";
        page = "subject_work.html";
    } else {
        keyword = "&person=";
        page = "person_work.html";
    }
    var displayDoc = window.open(page + "?auth=" + auth + keyword + d.id + "&url=" + url, "Node Connection Details");
}

function create_node() {
    if (create_node_parent && create_node_modal_active) {
        if (create_node_parent._children != null) {
            create_node_parent.children = create_node_parent._children;
            create_node_parent._children = null;
        }
        if (create_node_parent.children == null) {
            create_node_parent.children = [];
        }
        relation = $('#CreateNodeRelation').val();
        if (currentValue == "Work" || currentValue == "Subject") {
            id = $('#CreateNodeId1').val();
            sortorder = $('#CreateNodeOrder').val();
            name = $('#CreateNodeName').val();
            description = $('#CreateNodeDescription').val().replace(/(\r\n|\n|\r)/gm, "\r\n")
            new_node = {
                'name': name,
                'id': id,
                'sortorder': sortorder,
                'description': description,
                'relation': relation,
                'depth': create_node_parent.depth + 1,
                'children': [],
                '_children': null
            };
            create_node_parent.children.push(new_node);
            create_node_modal_active = false;
            // $('#CreateNodeId1').val('');
            // $('#CreateNodeName').val('');
            // $('#CreateNodeDescription').val('');
            // $('#CreateNodeOrder').val('');
        } else { // persons
            id = $('#CreateNodeId2').val();
            first = $('#CreateNodeFirst').val();
            middle = $('#CreateNodeMiddle').val();
            last = $('#CreateNodeLast').val();
            initials = $('#CreateNodeInitials').val();
            nick = $('#CreateNodeNick').val();
            other = $('#CreateNodeOther').val();
            if ($('#CreateNodeLiving').is(':checked')) living = '1';
            else living = '0';
            birth = $('#CreateNodeBirth').val();
            death = $('#CreateNodeDeath').val();
            biography = $('#CreateNodeBiography').val();
            new_node = {
                'id': id,
                'first': first,
                'middle': middle,
                'last': last,
                'initials': initials,
                'nick': nick,
                'other': other,
                'living': living,
                'birth': birth,
                'death': death,
                'biography': biography,
                'relation': relation,
                'depth': create_node_parent.depth + 1,
                'children': [],
                '_children': null
            };
            // $('#CreateNodeLabelStatus').text("Created Node " + id);
            create_node_parent.children.push(new_node);
            create_node_modal_active = false;
        }
        var auth = getauth();
        console.log('Created Node: ' + id);
        if (currentValue == "Subject") {
            with_relations = "subject-with-relation";
            d3.xhr(url + with_relations)
                .header("Content-Type", "application/json")
                .header("Authorization", "Basic " + btoa(auth))
                .post(
                    JSON.stringify({
                        "subject": { "id": new_node.id, "name": new_node.name, "description": new_node.description },
                        "related": create_node_parent.id,
                        "relation": new_node.relation,
                        "sortorder": new_node.sortorder
                    }),
                    function(err, rawdata) {
                        if (err) console.log("error:", err)
                        else {
                            try {
                                // var data = JSON.parse(str_replace(chr(13), str_replace(chr(10), rawdata)));
                                console.log("response:", rawdata.response, "status:", rawdata.status);
                            } catch (error) { console.log("error:", err, "response:", rawdata) };
                        }
                    }
                );
        } else if (currentValue == "Work") {
            with_relations = "work-with-relation";
            d3.xhr(url + with_relations)
                .header("Content-Type", "application/json")
                .header("Authorization", "Basic " + btoa(auth))
                .post(
                    JSON.stringify({
                        "work": { "id": new_node.id, "name": new_node.name, "description": new_node.description },
                        "related": create_node_parent.id,
                        "relation": new_node.relation,
                        "sortorder": new_node.sortorder
                    }),
                    function(err, rawdata) {
                        if (err) console.log("error:", err)
                        else {
                            try {
                                // var data = JSON.parse(str_replace(chr(13), str_replace(chr(10), rawdata)));
                                console.log("response:", rawdata.response, "status:", rawdata.status);
                            } catch (error) { console.log("error:", err, "response:", rawdata) };
                        }
                    }
                );
        } else { // persons
            with_relations = "person-with-relation";
            d3.xhr(url + with_relations)
                .header("Content-Type", "application/json")
                .header("Authorization", "Basic " + btoa(auth))
                .post(
                    JSON.stringify({
                        "person": {
                            "id": new_node.id,
                            "first": new_node.first,
                            "middle": new_node.middle,
                            "last": new_node.last,
                            "initials": new_node.initials,
                            "nick": new_node.nick,
                            "other": new_node.other,
                            "living": new_node.living,
                            "birth": new_node.birth,
                            "death": new_node.death,
                            "biography": new_node.biography
                        },
                        "related": create_node_parent.id,
                        "relation": new_node.relation
                    }),
                    function(err, rawdata) {
                        if (err) console.log("error:", err)
                        else {
                            try {
                                // var data = JSON.parse(str_replace(chr(13), str_replace(chr(10), rawdata)));
                                console.log("response:", rawdata.response, "status:", rawdata.status);
                            } catch (error) { console.log("error:", err, "response:", rawdata) };
                        }
                    }
                );
        }
        // console.log(subject_work_or_person);
        close_modal();
        outer_update(create_node_parent);
    }
}

function rename_node() {
    if (node_to_rename && rename_node_modal_active) {
        node_to_rename.relation = $('#RenameNodeRelation').val();
        if (currentValue == "Work" || currentValue == "Subject") {
            node_to_rename.id = $('#RenameNodeId1').val();
            node_to_rename.name = $('#RenameNodeName').val();
            node_to_rename.sortorder = $('#RenameNodeOrder').val();
            node_to_rename.description = $('#RenameNodeDescription').val();
        } else {
            node_to_rename.id = $('#RenameNodeId2').val();
            node_to_rename.first = $('#RenameNodeFirst').val();
            node_to_rename.middle = $('#RenameNodeMiddle').val();
            node_to_rename.last = $('#RenameNodeLast').val();
            node_to_rename.initials = $('#RenameNodeInitials').val();
            node_to_rename.nick = $('#RenameNodeNick').val();
            node_to_rename.other = $('#RenameNodeOther').val();
            if ($('#RenameNodeLiving').is(':checked')) node_to_rename.living = '1';
            else node_to_rename.living = '0';
            node_to_rename.birth = $('#RenameNodeBirth').val();
            node_to_rename.death = $('#RenameNodeDeath').val();
            node_to_rename.biography = $('#RenameNodeBiography').val();
        }
        var auth = getauth();
        if (currentValue == "Subject") {
            with_relations = "subject-with-relation";
            subject_work_or_person = "subject/";
            d3.xhr(url + subject_work_or_person + node_to_rename.id)
                .header("Content-Type", "application/json")
                .header("Authorization", "Basic " + btoa(auth))
                .send("PUT",
                    JSON.stringify({
                        "name": node_to_rename.name,
                        "description": node_to_rename.description,
                        "relation": node_to_rename.relation,
                        "sortorder": node_to_rename.sortorder
                    }),
                    function(err, rawdata) {
                        if (err) console.log("error:", err)
                        else {
                            try {
                                console.log("response:", rawdata.response, "status:", rawdata.status);
                            } catch (error) { console.log("error:", err, "response:", rawdata) };
                        }
                    }
                );
        } else if (currentValue == "Work") {
            with_relations = "work-with-relation";
            subject_work_or_person = "work/";
            d3.xhr(url + subject_work_or_person + node_to_rename.id)
                .header("Content-Type", "application/json")
                .header("Authorization", "Basic " + btoa(auth))
                .send("PUT",
                    JSON.stringify({
                        "name": node_to_rename.name,
                        "description": node_to_rename.description,
                        "relation": node_to_rename.relation,
                        "sortorder": node_to_rename.sortorder
                    }),
                    function(err, rawdata) {
                        if (err) console.log("error:", err)
                        else {
                            try {
                                console.log("response:", rawdata.response, "status:", rawdata.status);
                            } catch (error) { console.log("error:", err, "response:", rawdata) };
                        }
                    }
                );
        } else { // Person
            with_relations = "person-with-relation";
            subject_work_or_person = "person/";
            d3.xhr(url + subject_work_or_person + node_to_rename.id)
                .header("Content-Type", "application/json")
                .header("Authorization", "Basic " + btoa(auth))
                .send("PUT",
                    JSON.stringify({
                        "first": node_to_rename.first,
                        "middle": node_to_rename.middle,
                        "last": node_to_rename.last,
                        "initials": node_to_rename.initials,
                        "nick": node_to_rename.nick,
                        "other": node_to_rename.other,
                        "living": node_to_rename.living,
                        "birth": node_to_rename.birth,
                        "death": node_to_rename.death,
                        "biography": node_to_rename.biography,
                        "relation": node_to_rename.relation
                    }),
                    function(err, rawdata) {
                        if (err) console.log("error:", err)
                        else {
                            try {
                                console.log("response:", rawdata.response, "status:", rawdata.status);
                            } catch (error) { console.log("error:", err, "response:", rawdata) };
                        }
                    }
                );
        }
        console.log('Updated Node: ' + node_to_rename.id);
        rename_node_modal_active = false;
    }
    close_modal();
    outer_update(node_to_rename);
}

function move_node() {
    if (node_to_move_copy && move_node_modal_active) {
        $('#MoveNodeId').disabled = true;
        node_to_move_copy.id = $('#MoveNodeId').val();
        node_to_move_copy.parent = $('#MoveParentNode').val();
        node_to_move_copy.sortorder = $('#MoveNodeOrder').val();
        // console.log('Moving Node: ' + node_to_move_copy.id + ' To Node: ' + node_to_move_copy.parent);
        $('#MoveParentNodeId').val('');
        // var url = "http://127.0.0.1:5000/knowledgeTree/api/v1.0/";
        var auth = getauth();
        // if (subjects_works_or_persons_list == "works") move_copy_what = "subject-move/";
        if (currentValue == "Subject") move_copy_what = "subject-move/";
        else if (currentValue == "Work") move_copy_what = "work-move/";
        else move_copy_what = "person-move/"
        d3.xhr(url + move_copy_what + node_to_move_copy.id)
            .header("Content-Type", "application/json")
            .header("Authorization", "Basic " + btoa(auth))
            .post(
                JSON.stringify({
                    "id": node_to_move_copy.parent,
                    "sortorder": node_to_move_copy.sortorder
                }),
                function(err, rawdata) {
                    if (err) console.log("error:", err)
                    else {
                        try {
                            console.log("response:", rawdata.response, "status:", rawdata.status);
                        } catch (error) { console.log("error:", err, "response:", rawdata) };
                    }
                }
            );
        console.log('Moved Node: ' + node_to_move_copy.id + " Under: " + node_to_move_copy.parent + "order:" + node_to_move_copy.sortorder);
        move_node_modal_active = false;
        close_modal();
        outer_update(node_to_move_copy);
    }
}

function copy_node() {
    if (node_to_copy && copy_node_modal_active) {
        $('#CopyNodeId').disabled = true;
        node_to_copy.id = $('#CopyNodeId').val();
        node_to_copy.parent = $('#CopyParentNode').val();
        // console.log('Copying Node: ' + node_to_copy.id + ' To Node: ' + node_to_copy.parent);
        $('#CopyParentNodeId').val('');
        // var url = "http://127.0.0.1:5000/knowledgeTree/api/v1.0/";
        var auth = getauth();
        // if (subjects_works_or_persons_list == "works") copy_what = "subject-copy/";
        if (currentValue == "Subject") copy_what = "subject-copy/";
        else if (currentValue == "Subject") copy_what = "work-copy/";
        else copy_what = "person-copy/";
        d3.xhr(url + copy_what + node_to_copy.id)
            .header("Content-Type", "application/json")
            .header("Authorization", "Basic " + btoa(auth))
            .post(
                JSON.stringify({
                    "id": node_to_copy.parent,
                }),
                function(err, rawdata) {
                    if (err) console.log("error:", err)
                    else {
                        try {
                            console.log("response:", rawdata.response, "status:", rawdata.status);
                        } catch (error) { console.log("error:", err, "response:", rawdata) };
                    }
                }
            );
        console.log('Copied Node: ' + node_to_copy.id + " Under: " + node_to_copy.parent);
        copy_node_modal_active = false;
        close_modal();
        outer_update(node_to_copy);
    }
}
outer_update = null;

function draw_tree(error, treeData) {

    // Calculate total nodes, max label length
    var totalNodes = 0;
    var maxLabelLength = 0;
    // variables for drag/drop
    var selectedNode = null;
    var draggingNode = null;
    // panning variables
    var panSpeed = 200;
    var panBoundary = 20; // Within 20px from edges will pan when dragging.
    // Misc. variables
    var i = 0;
    var duration = 750;
    var root;

    // size of the diagram
    var viewerWidth = $(document).width();
    var viewerHeight = $(document).height();

    var tree = d3.layout.tree()
        .size([viewerHeight, viewerWidth]);

    // define a d3 diagonal projection for use by the node paths later on.
    var diagonal = d3.svg.diagonal()
        .projection(function(d) {
            return [d.y, d.x];
        });

    var menu = [{            title: 'View parent',
    action: function(elm, d, i) {
        var thekey;   
        if (d.parent!=="undefined") {
            if (currentValue == "Subject") thekey=d.parent.subject1;
            else if (currentValue == "Work") thekey=d.parent.work1;
            else thekey=d.parent.person1;
            if (typeof thekey=="undefined") thekey=d.parent.id;
        var auth = getauth();
        if (currentValue == "Subject") subtree = "subtree/";
        else if (currentValue == "Work") subtree = "subtree-work/";
        else subtree = "subtree-person/";
        d3.json(url + subtree + thekey).header("Authorization", "Basic " + btoa(auth)).get(function(err, content) {
            if (err) console.log("error:", err);
            else {
                svgElement = $("#tree-container").children().first();
                svgElement.remove();
                draw_tree(err, content);
            }
        });
    }}
},{
            title: 'View node',
            action: function(elm, d, i) {
                if (currentValue == "Subject" || currentValue == "Work") {
                    $('#ViewSubjectElements').show()
                    $('#ViewPersonElements').hide()
                    $("#ViewNodeId1").val(d.id);
                    $("#ViewNodeName").val(d.name);
                    $("#ViewNodeOrder").val(d.sortorder);
                    $("#ViewNodeDescription").val(d.description);
                    $("#ViewNodeId1").prop('disabled', true);
                    $("#ViewNodeName").prop('disabled', true);
                    $("#ViewNodeOrder").prop('disabled', true);
                    $("#ViewNodeDescription").prop('disabled', true);
                } else {
                    $('#ViewSubjectElements').hide();
                    $('#ViewPersonElements').show();
                    $("#ViewNodeId2").val(d.id);
                    $("#ViewNodeFirst").val(d.first);
                    $("#ViewNodeMiddle").val(d.middle);
                    $("#ViewNodeLast").val(d.last);
                    $("#ViewNodeInitials").val(d.initials);
                    $("#ViewNodeNick").val(d.nick);
                    $("#ViewNodeOther").val(d.other);
                    if (d.living == "1") {
                        $("#ViewNodeLiving").prop("checked", true);
                        $("#ViewNodeDeath").hide();
                        $("#ViewNodeLabelDeath").hide();
                    } else {
                        $("#ViewNodeLiving").prop("checked", false);
                        $("#ViewNodeDeath").show();
                        $("#ViewNodeLabelDeath").show();
                    }
                    $("#ViewNodeBirth").val(d.birth);
                    $("#ViewNodeDeath").val(d.death);
                    $("#ViewNodeBiography").val(d.biography);
                    $("#ViewNodeId2").prop('disabled', true);
                    $("#ViewNodeFirst").prop('disabled', true);
                    $("#ViewNodeMiddle").prop('disabled', true);
                    $("#ViewNodeLast").prop('disabled', true);
                    $("#ViewNodeInitials").prop('disabled', true);
                    $("#ViewNodeNick").prop('disabled', true);
                    $("#ViewNodeOther").prop('disabled', true);
                    $("#ViewNodeLiving").prop('disabled', true);
                    $("#ViewNodeBirth").prop('disabled', true);
                    $("#ViewNodeDeath").prop('disabled', true);
                    $("#ViewNodeBiography").prop('disabled', true);
                }
                $("#ViewNodeRelation").val(d.relation);
                view_node_modal_active = true;
                node_to_view = d;
                $("#ViewNodeName").focus();
                $('#ViewNodeModal').foundation('reveal', 'open');
            }
        },
        {
            title: 'Create child node',
            action: function(elm, d, i) {
                create_node_parent = d;
                create_node_modal_active = true;
                $("#CreateNodeLabelStatus").text('Status: Data entry in progress');
                $('#CreateNodeModal').foundation('reveal', 'open');
                if (currentValue == "Subject") {
                    $('#CreateSubjectElements').show();
                    $('#CreatePersonElements').hide();
                    $('#CreateNodeId1').val('');
                    $('#CreateNodeName').val('');
                    $('#CreateNodeDescription').val('');
                    $('#CreateNodeOrder').val('');
                    $('#CreateNodeRelation').val('Anga');
                } else if (currentValue == "Work") {
                    $('#CreateSubjectElements').show();
                    $('#CreatePersonElements').hide();
                    $('#CreateNodeId1').val('');
                    $('#CreateNodeName').val('');
                    $('#CreateNodeDescription').val('');
                    $('#CreateNodeOrder').val('');
                    $('#CreateNodeRelation').val('partwhole');
                } else {
                    $('#CreateSubjectElements').hide();
                    $('#CreatePersonElements').show();
                    $('#CreateNodeFirst').val('');
                    $('#CreateNodeMiddle').val('');
                    $('#CreateNodeLast').val('');
                    $('#CreateNodeInitials').val('');
                    $('#CreateNodeNick').val('');
                    $('#CreateNodeOther').val('');
                    $('#CreateNodeId2').val('');
                    $('#CreateNodeLiving').prop("checked", true);
                    $('#CreateNodeBirth').val('');
                    $('#CreateNodeDeath').val('');
                    $('#CreateNodeLabelDeath').hide();
                    $('#CreateNodeDeath').hide();
                    $('#CreateNodeBiography').val('');
                    $('#CreateNodeRelation').val('gurushishya');
                }
                promise_relations().then(); // refresh relations list
            }
        },
        {
            title: 'Edit node',
            action: function(elm, d, i) {
                if (currentValue == "Subject" || currentValue == "Work") {
                    $('#RenameSubjectElements').show();
                    $('#RenamePersonElements').hide();
                    $("#RenameNodeId1").val(d.id);
                    $("#RenameNodeName").val(d.name);
                    $("#RenameNodeOrder").val(d.sortorder);
                    $("#RenameNodeDescription").val(d.description);
                    $("#RenameNodeId1").prop('disabled', true);
                    $("#RenameNodeName").focus();
                } else {
                    $('#RenameSubjectElements').hide();
                    $('#RenamePersonElements').show();
                    $("#RenameNodeId2").val(d.id);
                    $("#RenameNodeFirst").val(d.first);
                    $("#RenameNodeMiddle").val(d.middle);
                    $("#RenameNodeLast").val(d.last);
                    $("#RenameNodeInitials").val(d.initials);
                    $("#RenameNodeNick").val(d.nick);
                    $("#RenameNodeOther").val(d.other);
                    $("#RenameNodeId2").prop('disabled', true);
                    if (d.living == "1") {
                        $("#RenameNodeLiving").prop("checked", true);
                        $("#RenameNodeDeath").hide();
                        $("#RenameNodeLabelDeath").hide();
                    } else {
                        $("#RenameNodeLiving").prop("checked", false);
                        $("#RenameNodeDeath").show();
                        $("#RenameNodeLabelDeath").show();
                    }
                    $("#RenameNodeBirth").val(d.birth);
                    $("#RenameNodeDeath").val(d.death);
                    $("#RenameNodeBiography").val(d.biography);
                    $("#RenameNodeFirst").focus();
                }
                $("#RenameNodeLabelStatus").text('Status: Data entry in progress');
                $("#RenameNodeRelation").val(d.relation);
                $('#RenameNodeModal').foundation('reveal', 'open');
                rename_node_modal_active = true;
                node_to_rename = d;
            }
        },
        {
            title: 'Remove node',
            action: function(elm, d, i) {
                delete_node(d);
            }
        },
        // {
        //     title: 'Collapse all nodes',
        //     action: function(elm, d, i) {
        //         collapseAllChildren(d);
        //     }
        // },
        {
            title: "Connect " + subjects_works_or_persons_list_sanskrit + " Node",
            action: function(elm, d, i) {
                if (currentValue == "Subject") {
                    // alert("case subjects");
                    $('#ConnectNodeSubjectElements').show();
                    $('#ConnectNodePersonElements').hide();
                    $("#ConnectWorkNode1").val('');
                    $("#ConnectSubjectNode").val(d.id);
                    $("#ConnectWorkNode").prop('disabled', false);
                    $("#ConnectSubjectNode").prop('disabled', true);
                    $('#ConnectSubjectNode').focus();
                } else if (currentValue == "Work") {
                    // alert("case works");
                    $('#ConnectNodeSubjectElements').show();
                    $('#ConnectNodePersonElements').hide();
                    $("#ConnectWorkNode1").val(d.id);
                    $("#ConnectSubjectNode").val('');
                    $("#ConnectWorkNode").prop('disabled', true);
                    $("#ConnectSubjectNode").prop('disabled', false);
                    $('#ConnectWorkNode').focus();
                } else {
                    $('#ConnectNodeSubjectElements').hide();
                    $('#ConnectNodePersonElements').show();
                    $("#ConnectPersonNode").val(d.id);
                    $("#ConnectWorkNode2").val('');
                    $("#ConnectPersonNode").prop('disabled', true);
                    $("#ConnectWorkNode2").prop('disabled', false);
                    $('#ConnectPersonNode').focus();
                }
                $("#ConnectNodeRelation").val("pramaana_pramatha");
                $('#ConnectNodeModal').foundation('reveal', 'open');
                connect_node_modal_active = true;
                // node_to_connect = d;
            }
        },
        {
            title: 'View ' + subjects_works_or_persons_list_sanskrit + ' Connections',
            action: function(elm, d, i) {
                showNodeConnectTree(d);
            }
        },
        {
            title: 'Move Subtree',
            action: function(elm, d, i) {
                move_node_modal_active = true;
                node_to_move_copy = d;
                getAllnodes(treeData, d.id);
                var count = allNodes.length;
                for (var i = 0; i < count; i++) {
                    $('#MoveParentList').append("<option value=\"" + allNodes[i] + "\"></option>");
                }
                $("#MoveNodeId").val(d.id);
                $("#MoveNodeOrder").val(d.sortorder);
                $('#MoveParentNodeId').focus();
                $('#MoveNodeModal').foundation('reveal', 'open');
            }
        },
        {
            title: 'Copy Subtree',
            action: function(elm, d, i) {
                copy_node_modal_active = true;
                node_to_copy = d;
                getAllnodes(treeData, d.id);
                var count = allNodes.length;
                for (var i = 0; i < count; i++) {
                    $('#CopyParentList').append("<option value=\"" + allNodes[i] + "\"></option>");
                }
                $("#CopyNodeId").val(d.id);
                $('#CopyParentNodeId').focus();
                $('#CopyNodeModal').foundation('reveal', 'open');
            }
        },
        {
            title: 'View Subtree',
            action: function(elm, d, i) {
                // var url = "http://127.0.0.1:5000/knowledgeTree/api/v1.0/";
                var auth = getauth();
                if (currentValue == "Subject") subtree = "subtree/";
                else if (currentValue == "Work") subtree = "subtree-work/";
                else subtree = "subtree-person/";
                d3.json(url + subtree + d.id).header("Authorization", "Basic " + btoa(auth)).get(function(err, content) {
                    if (err) console.log("error:", err);
                    else {
                        svgElement = $("#tree-container").children().first();
                        svgElement.remove();
                        draw_tree(err, content);
                    }
                });
            }
        },
        {
            title: 'Remove Subtree',
            action: function(elm, d, i) {
                delete_subtree(d);
            }
        }
    ]

    function getAllnodes(d, stopAt) {
        // if (typeof d.id != 'undefined') allNodes.push(d.id);
        if (d.id != stopAt) {
            allNodes.push(d.id);
            if (d.children) {
                var count = d.children.length;
                for (var i = 0; i < count; i++) {
                    getAllnodes(d.children[i], stopAt);
                }
            }
        }
    }

    // A recursive helper function for performing some setup by walking through all nodes

    function visit(parent, visitFn, childrenFn) {
        if (!parent) return;

        visitFn(parent);

        var children = childrenFn(parent);
        if (children) {
            var count = children.length;
            for (var i = 0; i < count; i++) {
                visit(children[i], visitFn, childrenFn);
            }
        }
    }

    // Call visit function to establish maxLabelLength
    visit(treeData, function(d) {
        totalNodes++;
        maxLabelLength = Math.max(d.id.length, maxLabelLength);

    }, function(d) {
        return d.children && d.children.length > 0 ? d.children : null;
    });

    function collapseAllChildren(node) {
        visit(treeData, function(d) {
                if (d.children) {
                    for (var child of d.children) {
                        collapse(child);
                        if (child == node) {
                            break;
                        }
                    }
                }
            },
            function(d) {
                return d.children && d.children.length > 0 ? d.children : null;
            });
    }


    function delete_node(node) {
        var auth = getauth();
        if (currentValue == "Subject") with_relations = "subject-with-relation/";
        else if (currentValue == "Work") with_relations = "work-with-relation/";
        else with_relations = "person-with-relation/";
        if (node.children || node._children) {
            alert("node has children, please use Remove Subtree!");
            return "Cancelled";}
        strconfirm = confirm("Are you sure you want to remove " + node.id);
        if (strconfirm == false) return 'Cancelled';
        d3.xhr(url + with_relations + node.id)
            .header("Content-Type", "application/json")
            .header("Authorization", "Basic " + btoa(auth))
            .send("DELETE",
                function(err, rawdata) {
                    if (err) console.log("error:", err)
                    else {
                        try {
                            // var data = JSON.parse(str_replace(chr(13), str_replace(chr(10), rawdata)));
                            console.log("response:", rawdata.response, "status:", rawdata.status);
                        } catch (error) { console.log("error:", err, "response:", rawdata) };
                        visit(treeData, function(d) {
                                if (d.children) {
                                    for (var child of d.children) {
                                        if (child == node) {
                                            d.children = _.without(d.children, child);
                                            update(root);
                                            break;
                                        }
                                    }
                                }
                            },
                            function(d) {
                                return d.children && d.children.length > 0 ? d.children : null;
                            });
                    }
                });
        console.log('Removed Node id: ' + node.id);
    }

    function delete_subtree(node) {
        // var url = "http://127.0.0.1:5000/knowledgeTree/api/v1.0/";
        var auth = getauth();
        if (currentValue == "Subject") subtree = "subtree/";
        else if (currentValue == "Work") subtree = "subtree-work/";
        else subtree = "subtree-person/";
        if (!(node.children || node._children)) {
            alert("node does not have children, please use Remove Node!");
            return "Cancelled";}
        strconfirm = confirm("Are you sure you want to remove subtree " + node.id);
        if (strconfirm == false) return 'Cancelled';
        d3.xhr(url + subtree + node.id)
            .header("Content-Type", "application/json")
            .header("Authorization", "Basic " + btoa(auth))
            .send("DELETE",
                function(err, rawdata) {
                    if (err) console.log("error:", err)
                    else {
                        try {
                            // var data = JSON.parse(str_replace(chr(13), str_replace(chr(10), rawdata)));
                            console.log("response:", rawdata.response, "status:", rawdata.status);
                        } catch (error) { console.log("error:", err, "response:", rawdata) };
                        visit(treeData, function(d) {
                                if (d.children) {
                                    for (var child of d.children) {
                                        if (child == node) {
                                            d.children = _.without(d.children, child);
                                            update(root);
                                            break;
                                        }
                                    }
                                }
                            },
                            function(d) {
                                return d.children && d.children.length > 0 ? d.children : null;
                            });
                    }
                });
        console.log('Removed Subtree id: ' + node.id);
    }


    // sort the tree according to the node names

    function sortTree() {
        tree.sort(function(a, b) {
            if (currentValue == "Person") return b.id.toLowerCase() < a.id.toLowerCase() ? 1 : -1;
            var b_order = b.sortorder;
            if (typeof(b_order) == "string") {
                if (b_order.length < 2) b_order = "0" + b_order;
            }

            var a_order = a.sortorder;
            if (typeof(a_order) == "string") {
                if (a_order.length < 2) a_order = "0" + a_order;
            }

            return b_order < a_order ? 1 : -1;
            // return b.sortorder < a.sortorder ? 1 : -1;
        });
    }
    // Sort the tree initially incase the JSON isn't in a sorted order.
    sortTree();

    // TODO: Pan function, can be better implemented.

    function pan(domNode, direction) {
        var speed = panSpeed;
        if (panTimer) {
            clearTimeout(panTimer);
            translateCoords = d3.transform(svgGroup.attr("transform"));
            if (direction == 'left' || direction == 'right') {
                translateX = direction == 'left' ? translateCoords.translate[0] + speed : translateCoords.translate[0] - speed;
                translateY = translateCoords.translate[1];
            } else if (direction == 'up' || direction == 'down') {
                translateX = translateCoords.translate[0];
                translateY = direction == 'up' ? translateCoords.translate[1] + speed : translateCoords.translate[1] - speed;
            }
            scaleX = translateCoords.scale[0];
            scaleY = translateCoords.scale[1];
            scale = zoomListener.scale();
            svgGroup.transition().attr("transform", "translate(" + translateX + "," + translateY + ")scale(" + scale + ")");
            d3.select(domNode).select('g.node').attr("transform", "translate(" + translateX + "," + translateY + ")");
            zoomListener.scale(zoomListener.scale());
            zoomListener.translate([translateX, translateY]);
            panTimer = setTimeout(function() {
                pan(domNode, speed, direction);
            }, 50);
        }
    }

    // Define the zoom function for the zoomable tree

    function zoom() {
        svgGroup.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
    }


    // define the zoomListener which calls the zoom function on the "zoom" event constrained within the scaleExtents
    var zoomListener = d3.behavior.zoom().scaleExtent([0.1, 3]).on("zoom", zoom);

    function move_copy_node(node_to_move_copy, theparent) {
        strconfirm = confirm("Are you sure you want to move/copy " + node_to_move_copy + " to " + theparent);
        if (strconfirm == false) return 'Cancelled';
        var auth = getauth();
        strconfirm = confirm("Click Ok to Copy - OR - Cancel to Move :-) " + node_to_move_copy + " to " + theparent);
        if (strconfirm == false) {
            movecopy = "Moved";
            if (currentValue == "Subject") move_copy_what = "subject-move/";
            else if (currentValue == "Work") move_copy_what = "work-move/";
            else move_copy_what = "person-move/";
        } else {
            movecopy = "Copied";
            if (currentValue == "Subject") move_copy_what = "subject-copy/";
            else if (currentValue == "Work") move_copy_what = "work-copy/";
            else move_copy_what = "person-copy/";
        }
        d3.xhr(url + move_copy_what + node_to_move_copy)
            .header("Content-Type", "application/json")
            .header("Authorization", "Basic " + btoa(auth))
            .post(
                JSON.stringify({
                    "id": theparent
                }),
                function(err, rawdata) {
                    if (err) console.log("error:", err)
                    else {
                        try {
                            console.log("response:", rawdata.response, "status:", rawdata.status);
                        } catch (error) { console.log("error:", err, "response:", rawdata) };
                    }
                }
            );
        console.log(movecopy + ' Node: ' + node_to_move_copy + " Under: " + theparent);
        return movecopy;
    }

    function initiateDrag(d, domNode) {
        draggingNode = d;
        d3.select(domNode).select('.ghostCircle').attr('pointer-events', 'none');
        d3.selectAll('.ghostCircle').attr('class', 'ghostCircle show');
        d3.select(domNode).attr('class', 'node activeDrag');

        svgGroup.selectAll("g.node").sort(function(a, b) { // select the parent and sort the path's
            if (a.id != draggingNode.id) return 1; // a is not the hovered element, send "a" to the back
            else return -1; // a is the hovered element, bring "a" to the front
        });
        // if nodes has children, remove the links and nodes
        if (nodes.length > 1) {
            // remove link paths
            links = tree.links(nodes);
            nodePaths = svgGroup.selectAll("path.link")
                .data(links, function(d) {
                    return d.target.id;
                }).remove();
            // remove child nodes
            nodesExit = svgGroup.selectAll("g.node")
                .data(nodes, function(d) {
                    return d.id;
                }).filter(function(d, i) {
                    if (d.id == draggingNode.id) {
                        return false;
                    }
                    return true;
                }).remove();
        }

        // remove parent link
        parentLink = tree.links(tree.nodes(draggingNode.parent));
        svgGroup.selectAll('path.link').filter(function(d, i) {
            if (d.target.id == draggingNode.id) {
                return true;
            }
            return false;
        }).remove();

        dragStarted = null;
    }

    // define the baseSvg, attaching a class for styling and the zoomListener
    var baseSvg = d3.select("#tree-container").append("svg")
        .attr("width", viewerWidth)
        .attr("height", viewerHeight);

    baseSvg.append("rect")
        .attr("width", "100%")
        .attr("height", "100%")
        .attr("fill", "white")

    baseSvg.call(zoomListener);


    // Define the drag listeners for drag/drop behaviour of nodes.
    dragListener = d3.behavior.drag()
        .on("dragstart", function(d) {
            if (d == root) {
                return;
            }
            dragStarted = true;
            nodes = tree.nodes(d);
            d3.event.sourceEvent.stopPropagation();
            // it's important that we suppress the mouseover event on the node being dragged. Otherwise it will absorb the mouseover event and the underlying node will not detect it d3.select(this).attr('pointer-events', 'none');
        })
        .on("drag", function(d) {
            if (d == root) {
                return;
            }
            if (dragStarted) {
                domNode = this;
                initiateDrag(d, domNode);
            }

            // get coords of mouseEvent relative to svg container to allow for panning
            relCoords = d3.mouse($('svg').get(0));
            if (relCoords[0] < panBoundary) {
                panTimer = true;
                pan(this, 'left');
            } else if (relCoords[0] > ($('svg').width() - panBoundary)) {

                panTimer = true;
                pan(this, 'right');
            } else if (relCoords[1] < panBoundary) {
                panTimer = true;
                pan(this, 'up');
            } else if (relCoords[1] > ($('svg').height() - panBoundary)) {
                panTimer = true;
                pan(this, 'down');
            } else {
                try {
                    clearTimeout(panTimer);
                } catch (e) {

                }
            }

            d.x0 += d3.event.dy;
            d.y0 += d3.event.dx;
            var node = d3.select(this);
            node.attr("transform", "translate(" + d.y0 + "," + d.x0 + ")");
            updateTempConnector();
        }).on("dragend", function(d) {
            if (d == root) {
                return;
            }
            domNode = this;
            if (selectedNode) {
                response = move_copy_node(draggingNode.id, selectedNode.id);
                if (response == 'Moved') {
                    // now remove the element from the parent, and insert it into the new elements children
                    var index = draggingNode.parent.children.indexOf(draggingNode);
                    if (index > -1) {
                        draggingNode.parent.children.splice(index, 1);
                    }
                    if ((selectedNode.children == null) &&
                        (selectedNode._children == null)) {
                        selectedNode.children = [];
                        selectedNode.children.push(draggingNode);
                    } else {
                        if (selectedNode._children == null)
                            selectedNode.children.push(draggingNode);
                        else
                            selectedNode._children.push(draggingNode);
                    }
                    // Make sure that the node being added to is expanded so user can see added node is correctly moved
                    expand(selectedNode);
                    sortTree();
                    endDrag();
                } else if (response == 'Copied') {
                    // var index = draggingNode.parent.children.indexOf(draggingNode);
                    // if (index > -1) {
                    // draggingNode.parent.children.splice(index, 1);
                    // }
                    // console.log(draggingNode);
                    if ((selectedNode.children == null) &&
                        (selectedNode._children == null)) {
                        selectedNode.children = [];
                        if (draggingNode.children == null)
                            draggingNode._children.forEach(function(item) { selectedNode.children.push(item); });
                        else draggingNode.children.forEach(function(item) { selectedNode.children.push(item); });
                    } else {
                        if (selectedNode._children == null) {
                            if (draggingNode.children == null)
                                draggingNode._children.forEach(function(item) { selectedNode.children.push(item); });
                            else draggingNode.children.forEach(function(item) { selectedNode.children.push(item); });
                        } else {
                            if (draggingNode.children == null)
                                draggingNode._children.forEach(function(item) { selectedNode.children.push(item); });
                            else draggingNode.children.forEach(function(item) { selectedNode.children.push(item); });
                        }
                    }
                    // Make sure that the node being added to is expanded so user can see added node is correctly moved
                    expand(selectedNode);
                    // expand(draggingNode);
                    sortTree();
                    endDrag();
                }
            } else {
                endDrag();
            }
        });

    function endDrag() {
        selectedNode = null;
        d3.selectAll('.ghostCircle').attr('class', 'ghostCircle');
        d3.select(domNode).attr('class', 'node');
        // now restore the mouseover event or we won't be able to drag a 2nd time
        d3.select(domNode).select('.ghostCircle').attr('pointer-events', '');
        updateTempConnector();
        if (draggingNode !== null) {
            update(root);
            centerNode(draggingNode);
            draggingNode = null;
        }
    }

    // Helper functions for collapsing and expanding nodes.

    function collapse(d) {
        if (d.children) {
            d._children = d.children;
            d._children.forEach(collapse);
            d.children = null;
        }
    }

    function expand(d) {
        if (d._children) {
            d.children = d._children;
            d.children.forEach(expand);
            d._children = null;
        }
    }

    var overCircle = function(d) {
        selectedNode = d;
        updateTempConnector();
    };
    var outCircle = function(d) {
        selectedNode = null;
        updateTempConnector();
    };

    // color a node properly
    function colorNode(d) {
        // result = "#fff";
        /*        if (d.synthetic == true) {
                    result = (d._children || d.children) ? "darkgray" : "lightgray";
                } else {
                    if (d.type == "USDA") {
                        result = (d._children || d.children) ? "orangered" : "orange";
                    } else if (d.type == "Produce") {
                        result = (d._children || d.children) ? "yellowgreen" : "yellow";
                    } else if (d.type == "RecipeIngredient") {
                        result = (d._children || d.children) ? "skyblue" : "royalblue";
                    } else {
                        result = "lightsteelblue"
                    }
                }
        */
        result = (d._children || d.children) ? "darkgray" : "white";
        return result;
    }

    function colorLink(d) {
        console.log("link relation:", d.relation)
        switch (d.relation) {
            case "Anga":
                result = "lightgray";
                break;
            case "Avayavi":
                result = "orange";
                break;
            default:
                result = "black"
        }
        return result;
    }
    // Function to update the temporary connector indicating dragging affiliation
    var updateTempConnector = function() {
        var data = [];
        if (draggingNode !== null && selectedNode !== null) {
            // have to flip the source coordinates since we did this for the existing connectors on the original tree
            data = [{
                source: {
                    x: selectedNode.y0,
                    y: selectedNode.x0
                },
                target: {
                    x: draggingNode.y0,
                    y: draggingNode.x0
                }
            }];
        }
        var link = svgGroup.selectAll(".templink").data(data);

        link.enter().append("path")
            .attr("class", "templink")
            .attr("d", d3.svg.diagonal())
            .attr('pointer-events', 'none');

        link.attr("d", d3.svg.diagonal());

        link.exit().remove();
    };

    // Function to center node when clicked/dropped so node doesn't get lost when collapsing/moving with large amount of children.

    function centerNode(source) {
        scale = zoomListener.scale();
        x = -source.y0;
        y = -source.x0;
        x = x * scale + viewerWidth / 2;
        y = y * scale + viewerHeight / 2;
        d3.select('g').transition()
            .duration(duration)
            .attr("transform", "translate(" + x + "," + y + ")scale(" + scale + ")");
        zoomListener.scale(scale);
        zoomListener.translate([x, y]);
    }

    // Toggle children function

    function toggleChildren(d) {
        if (d.children) {
            d._children = d.children;
            d.children = null;
        } else if (d._children) {
            d.children = d._children;
            d._children = null;
        }
        return d;
    }

    // Toggle children on click.

    function click(d) {
        if (d3.event.defaultPrevented) return; // click suppressed
        d = toggleChildren(d);
        update(d);
        centerNode(d);
    }

    function showNodeAsWebPage(d) {
        var displayDoc = window.open("", "Node Details"); //, "width=800,height=500"); //"displayNode.html");
        if (currentValue == "Subject" || currentValue == "Work")
            displayDoc.document.write("<head><title>" + d.name + "</title></head><body>" +
                "<h2>Name:" + d.name + "</h2><br/>" + "<p>Description:" + d.description + "</p><body>");
        else {
            if (typeof(d.first) == "undefined") f = "";
            else f = d.first;
            if (typeof(d.middle) == "undefined") m = "";
            else m = d.middle;
            if (typeof(d.last) == "undefined") l = "";
            else l = d.last;
            if (typeof(d.birth) == "undefined") birth = "birth:unknown";
            else birth = "birth:" + d.birth;
            if (typeof(d.death) == "undefined") death = "death:unknown";
            else death = d.death;
            if (typeof(d.living) == "undefined") death = "death:unknown";
            else if (d.living == 1) death = "";
            if (typeof(d.biography) == "undefined") biography = "unknown";
            else biography = d.biography;
            displayDoc.document.write("<head><title>" + f + ' ' + m + ' ' + l + "</title></head><body>" +
                "<h2>Name:" + f + ' ' + m + ' ' + l + "</h2><br/>" +
                "<p>" + birth + death + "<br/>" +
                "<p>Biography:" + biography +
                "</p><body>");
        }
    }

    function update(source) {
        // Compute the new height, function counts total children of root node and sets tree height accordingly.
        // This prevents the layout looking squashed when new nodes are made visible or looking sparse when nodes are removed
        // This makes the layout more consistent.
        var levelWidth = [1];
        var childCount = function(level, n) {

            if (n.children && n.children.length > 0) {
                if (levelWidth.length <= level + 1) levelWidth.push(0);

                levelWidth[level + 1] += n.children.length;
                n.children.forEach(function(d) {
                    childCount(level + 1, d);
                });
            }
        };
        childCount(0, root);
        var newHeight = d3.max(levelWidth) * 25; // 25 pixels per line  
        tree = tree.size([newHeight, viewerWidth]);

        // Compute the new tree layout.
        var nodes = tree.nodes(root).reverse(),
            links = tree.links(nodes);

        // Set widths between levels based on maxLabelLength.
        nodes.forEach(function(d) {
            //d.y = (d.depth * (maxLabelLength * 10)); //maxLabelLength * 10px
            // alternatively to keep a fixed scale one can set a fixed depth per level
            // Normalize for fixed-depth by commenting out below line
            d.y = (d.depth * 300); //500px per level.
        });

        // Update the nodes…
        node = svgGroup.selectAll("g.node")
            .data(nodes, function(d) {
                return d.id || (d.id = ++i);
            });

        // Enter any new nodes at the parent's previous position.
        var nodeEnter = node.enter().append("g")
            .call(dragListener)
            .attr("class", "node")
            .attr("transform", function(d) {
                return "translate(" + source.y0 + "," + source.x0 + ")";
            })
            .on('click', click);

        nodeEnter.append("circle")
            .attr('class', 'nodeCircle')
            .attr("r", 0)
            .style("fill", colorNode);

        nodeEnter.append("text")
            .attr("x", function(d) {
                return d.children || d._children ? -10 : 10;
            })
            .attr("dy", ".35em")
            .attr('class', 'nodeText')
            .attr("text-anchor", function(d) {
                return d.children || d._children ? "end" : "start";
            })
            .text(function(d) {
                // console.log(currentValue, d.id);
                if (currentValue == "Person") {
                    if (typeof(d.first) == "undefined") f = "";
                    else f = d.first;
                    if (typeof(d.middle) == "undefined") m = "";
                    else m = d.middle;
                    if (typeof(d.last) == "undefined") l = "";
                    else l = d.last;
                    return f + ' ' + m + ' ' + l;
                } else return d.name;
            })
            .style("fill-opacity", 0)
            .on('click', showNodeAsWebPage);

        // phantom node to give us mouseover in a radius around it
        nodeEnter.append("circle")
            .attr('class', 'ghostCircle')
            .attr("r", 30)
            .attr("opacity", 0.2) // change this to zero to hide the target area
            .style("fill", "red")
            .attr('pointer-events', 'mouseover')
            .on("mouseover", function(node) {
                overCircle(node);
            })
            .on("mouseout", function(node) {
                outCircle(node);
            });

        // Update the text to reflect whether node has children or not.
        node.select('text')
            .attr("x", function(d) {
                return d.children || d._children ? -10 : 10;
            })
            .attr("text-anchor", function(d) {
                return d.children || d._children ? "end" : "start";
            })
            .text(function(d) {
                if (currentValue == "Person") {
                    if (typeof(d.first) == "undefined") f = "";
                    else f = d.first;
                    if (typeof(d.middle) == "undefined") m = "";
                    else m = d.middle;
                    if (typeof(d.last) == "undefined") l = "";
                    else l = d.last;
                    return f + ' ' + m + ' ' + l;
                }
                return d.name;
            });

        // Change the circle fill depending on whether it has children and is collapsed
        node.select("circle.nodeCircle")
            .attr("r", 4.5)
            .style("fill", colorNode);

        // Add a context menu
        node.on('contextmenu', d3.contextMenu(menu));


        // Transition nodes to their new position.
        var nodeUpdate = node.transition()
            .duration(duration)
            .attr("transform", function(d) {
                return "translate(" + d.y + "," + d.x + ")";
            });

        // Fade the text in
        nodeUpdate.select("text")
            .style("fill-opacity", 1);

        // Transition exiting nodes to the parent's new position.
        var nodeExit = node.exit().transition()
            .duration(duration)
            .attr("transform", function(d) {
                return "translate(" + source.y + "," + source.x + ")";
            })
            .remove();

        nodeExit.select("circle")
            .attr("r", 0);

        nodeExit.select("text")
            .style("fill-opacity", 0);

        // Update the links…
        var link = svgGroup.selectAll("path.link")
            .data(links, function(d) {
                return d.target.id;
            });

        // Enter any new links at the parent's previous position.
        link.enter().insert("path", "g")
            .attr("class", "link")
            .attr("d", function(d) {
                var o = {
                    x: source.x0,
                    y: source.y0
                };
                return diagonal({
                    source: o,
                    target: o
                });
            });

        // Transition links to their new position.
        link.transition()
            .duration(duration)
            .attr("d", diagonal);

        // Transition exiting nodes to the parent's new position.
        link.exit().transition()
            .duration(duration)
            .attr("d", function(d) {
                var o = {
                    x: source.x,
                    y: source.y
                };
                return diagonal({
                    source: o,
                    target: o
                });
            })
            .remove();

        // Stash the old positions for transition.
        nodes.forEach(function(d) {
            d.x0 = d.x;
            d.y0 = d.y;
        });
    }

    outer_update = update;

    // Append a group which holds all nodes and which the zoom Listener can act upon.
    var svgGroup = baseSvg.append("g");

    // Define the root
    root = treeData;
    root.x0 = viewerHeight / 2;
    root.y0 = 0;

    // Layout the tree initially and center on the root node.
    collapseAllChildren(root);
    update(root);
    centerNode(root);
    tree_root = root;
}