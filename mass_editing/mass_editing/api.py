import frappe, json
import frappe.model.meta
from frappe import _
from frappe.utils import cstr, unique, nowdate, add_days

# this is called by the Link Field
@frappe.whitelist()
def search_link(doctype, txt, query=None, filters=None, page_length=20, searchfield=None):
    search_widget(doctype, txt, query, searchfield=searchfield, page_length=page_length, filters=filters)
    frappe.response['results'] = build_for_autosuggest(frappe.response["values"])
    del frappe.response["values"]

# this is called by the search box
@frappe.whitelist()
def search_widget(doctype, txt, query=None, searchfield=None, start=0,
    page_length=100, filters=None, filter_fields=None, as_dict=False):
    if isinstance(filters, basestring):
        filters = json.loads(filters)

    meta = frappe.get_meta(doctype)

    if not searchfield:
        searchfield = "name"

    standard_queries = frappe.get_hooks().standard_queries or {}

    if query and query.split()[0].lower()!="select":
        # by method
        frappe.response["values"] = frappe.call(query, doctype, txt,
            searchfield, start, page_length, filters, as_dict=as_dict)
    elif not query and doctype in standard_queries:
        # from standard queries
        search_widget(doctype, txt, standard_queries[doctype][0],
            searchfield, start, page_length, filters)
    else:
        if query:
            frappe.throw(_("This query style is discontinued"))
            # custom query
            # frappe.response["values"] = frappe.db.sql(scrub_custom_query(query, searchfield, txt))
        else:
            if isinstance(filters, dict):
                filters_items = filters.items()
                filters = []
                for f in filters_items:
                    if isinstance(f[1], (list, tuple)):
                        filters.append([doctype, f[0], f[1][0], f[1][1]])
                    else:
                        filters.append([doctype, f[0], "=", f[1]])

            if filters==None:
                filters = []
            or_filters = []


            # build from doctype
            if txt:
                if doctype == "DocField":
                    search_fields = ["name", "fieldname", "label"]
                else:
                    search_fields = ["name"]
                if meta.title_field:
                    search_fields.append(meta.title_field)

                if meta.search_fields:
                    search_fields.extend(meta.get_search_fields())

                for f in search_fields:
                    fmeta = meta.get_field(f.strip())
                    if f == "name" or (fmeta and fmeta.fieldtype in ["Data", "Text", "Small Text", "Long Text",
                        "Link", "Select", "Read Only", "Text Editor"]):
                            or_filters.append([doctype, f.strip(), "like", "%{0}%".format(txt)])

            if meta.get("fields", {"fieldname":"enabled", "fieldtype":"Check"}):
                filters.append([doctype, "enabled", "=", 1])
            if meta.get("fields", {"fieldname":"disabled", "fieldtype":"Check"}):
                filters.append([doctype, "disabled", "!=", 1])

            # format a list of fields combining search fields and filter fields
            fields = get_std_fields_list(meta, searchfield or "name")
            if filter_fields:
                fields = list(set(fields + json.loads(filter_fields)))
            formatted_fields = ['`tab%s`.`%s`' % (meta.name, f.strip()) for f in fields]

            # find relevance as location of search term from the beginning of string `name`. used for sorting results.
            formatted_fields.append("""locate("{_txt}", `tab{doctype}`.`name`) as `_relevance`""".format(
                _txt=frappe.db.escape((txt or "").replace("%", "")), doctype=frappe.db.escape(doctype)))


            # In order_by, `idx` gets second priority, because it stores link count
            from frappe.model.db_query import get_order_by
            order_by_based_on_meta = get_order_by(doctype, meta)
            order_by = "if(_relevance, _relevance, 99999), idx desc, {0}".format(order_by_based_on_meta)

            values = frappe.get_list(doctype,
                filters=filters, fields=formatted_fields,
                or_filters = or_filters, limit_start = start,
                limit_page_length=page_length,
                order_by=order_by,
                ignore_permissions = True if doctype == "DocType" else False, # for dynamic links
                as_list=not as_dict)

            # remove _relevance from results
            if as_dict:
                for r in values:
                    r.pop("_relevance")
                frappe.response["values"] = values
            else:
                frappe.response["values"] = [r[:-1] for r in values]

def get_std_fields_list(meta, key):
    # get additional search fields
    sflist = meta.search_fields and meta.search_fields.split(",") or []
    title_field = [meta.title_field] if (meta.title_field and meta.title_field not in sflist) else []
    sflist = ['name'] + sflist + title_field
    if not key in sflist:
        sflist = sflist + [key]

    return sflist

def build_for_autosuggest(res):
    results = []
    for r in res:
        out = {"value": r[0], "description": ", ".join(unique(cstr(d) for d in r if d)[1:])}
        results.append(out)
    return results


@frappe.whitelist()
def update_doc_records_by_mass_editing(args=None):
    if not args:
        args = frappe.local.form_dict
    ignore_keys = ['cmd', 'selected_doc_records', 'doctype']
    if args and args.get('doctype', False) and args.get('selected_doc_records', False):
        for doc_id in eval(args['selected_doc_records']):
            for field_name in args.keys():
                # This code is add fields in args because some fields is not
                # comes by default in args if fields value is not selected
                # in mass editing dialog box
                if field_name.startswith('select_'):
                    split_field_name = field_name.split('select_')
                    if args.get(field_name, False) == 'Remove' and len(\
                        split_field_name) >= 2 and args.get(
                            split_field_name[1], False):
                        if args.get(str(split_field_name[1]), False):
                            frappe.throw(_(
                                "You can not fill field value "
                                "when "
                                "Select Or Remove Type is ' Remove '. "
                                "Please make it blank for Remove "
                                "type of fields. [' "
                                "%s ' ]") % str(split_field_name[1]))
                    if len(split_field_name) >= 2 and not args.get(
                        split_field_name[1], False):
                        if args.get(field_name, False) == 'Set':
                            if not args.get(str(split_field_name[1]), False):
                                frappe.throw(_(
                                    "You can not set blank field value when "
                                    "Select Or Remove Type is ' Set '. Please "
                                    "fill value for Set type of fields. [' "
                                    "%s ' ]") % str(split_field_name[1]))
                        fields_type_details = frappe.db.sql(
                            """select fieldname,fieldtype,options from
							`tabDocField` where fieldname=%s and parent=%s""",
                            (str(split_field_name[1]), str(args['doctype'])))
                        if fields_type_details and fields_type_details[0] and \
                            len(fields_type_details[0]) >= 3:
                            if fields_type_details[0][1] in ['Date',
                                'Datetime', 'Check', 'Link', 'Data',
                                'Currency', 'Attach', 'Attach Image',
                                'Color', 'Time', 'Password', 'Signature']:
                                args[split_field_name[1]] = None
                            if fields_type_details[0][1] in ['Float',
                                                             'Percent']:
                                args[split_field_name[1]] = 0.0
                            if fields_type_details[0][1] in ['Int']:
                                args[split_field_name[1]] = 0
                            if fields_type_details[0][1] in ['Select',
                                 'Text', 'Small Text', 'Long Text',
                                 'Text Editor', 'Code']:
                                args[split_field_name[1]] = ""
                            
            for field_name in args.keys():
                # This code is update or remove fields values from selected
                # doctype records.
                if not field_name.startswith('select_') and field_name not in ignore_keys:
                    if str(args['select_'+str(field_name)]) == 'Set' and args[field_name]:
                        frappe.db.set_value(str(args['doctype']), str(doc_id),
                                                field_name, args[field_name])
                    
                    if str(args['select_' + str(field_name)]) == 'Remove':
                        frappe.db.set_value(str(args['doctype']),
                                    str(doc_id), field_name, args[field_name])
                

@frappe.whitelist()
def get_fields_for_mass_editing(args=None):
    if not args:
        args = frappe.local.form_dict
    mass_edit_dialog_fields = {'mass_fields' : []}
    if args and args.get('mass_doctype', False) and args.get('doctype', False):
        mass_recs = frappe.db.sql("""select name from `tabMass Editing`
                                where model_id=%s""", (args['doctype']))
        if mass_recs and mass_recs[0] and mass_recs[0][0]:
            mass_doc_rec = frappe.get_doc(str(args['mass_doctype']),
                                          str(mass_recs[0][0]))
            if mass_doc_rec.fields_ids:
                for field in mass_doc_rec.fields_ids:
                    if field.mass_doctype_field:
                        field_name = field.mass_doctype_field
                        mass_doc_field_rec = frappe.get_doc(
                            'DocField', field_name)
                        mass_edit_dialog_fields['mass_fields'].append({
                            'fieldtype': 'Select',
                            'fieldname': 'select_'
                                         + str(mass_doc_field_rec.fieldname),
                            'label': "Select Or Remove "+ str(
                                mass_doc_field_rec.label),
                            'options': [{'value': 'Set', 'label':'Set'},
                                        {'value': 'Remove', 'label':
                                            'Remove'}],
                            'default': 'Set'
                        })
                        mass_edit_dialog_fields['mass_fields'].append({
                            'fieldtype': 'Column Break'})
                        mass_edit_dialog_fields['mass_fields'].append({
                            'fieldtype': mass_doc_field_rec.fieldtype,
                            'fieldname': mass_doc_field_rec.fieldname,
                            'label': mass_doc_field_rec.label,
                            'reqd': 0,
                            # 'read_only': mass_doc_field_rec.read_only,
                            'bold': mass_doc_field_rec.bold,
                            'options':mass_doc_field_rec.options or ''
                        })
                        mass_edit_dialog_fields['mass_fields'].append({
                            'fieldtype': 'Section Break'})
            else:
                frappe.throw(_("Mass Editing Lines (fields) is not configured "
                               "for ' "
                               "%s ' "
                               "doctype. "
                               "Please configure it first from mass editing "
                               "menu.") %
                             str(args['doctype']))
            return mass_edit_dialog_fields
        else:
            frappe.throw(_("Mass Editing is not configured for ' %s ' "
                           "doctype. "
                           "Please configure it first from mass editing "
                           "menu.")%
                         str(args['doctype']))
