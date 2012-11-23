#!/usr/bin/env python
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

__license__   = 'Free to use for personal use'
__copyright__ = '2012, Daniel Bratell <bratell@lysator.liu.se>'
__docformat__ = 'restructuredtext en'

from PyQt4.Qt import QDialog, QVBoxLayout, QPushButton, QMessageBox, QLabel

from calibre_plugins.tag_stats_plugin.config import prefs
from calibre_plugins.tag_stats_plugin.chart_dialog import ChartDialog
from operator import itemgetter
import fnmatch
import re
import string

class TagStatsDialog(QDialog):

    def __init__(self, gui, icon, do_user_config):
        QDialog.__init__(self, gui)
        self.gui = gui
        self.do_user_config = do_user_config
        self.icon = icon

        # The current database shown in the GUI
        # db is an instance of the class LibraryDatabase2 from database.py
        # This class has many, many methods that allow you to do a lot of
        # things.
        self.db = gui.current_db

        self.l = QVBoxLayout()
        self.setLayout(self.l)

        self.label = QLabel(prefs['hello_world_msg'])
        self.l.addWidget(self.label)

        self.setWindowTitle('Tag Stats Prototype')
        self.setWindowIcon(icon)

        self.about_button = QPushButton('About', self)
        self.about_button.clicked.connect(self.about)
        self.l.addWidget(self.about_button)

        self.count_genres_button = QPushButton(
            'Count genres and locations', self)
        self.count_genres_button.clicked.connect(self.count_genres)
        self.l.addWidget(self.count_genres_button)

        self.marked_button = QPushButton(
            'Show books with only one format in the calibre GUI', self)
        self.marked_button.clicked.connect(self.marked)
        self.l.addWidget(self.marked_button)

        self.view_button = QPushButton(
            'View the most recently added book', self)
        self.view_button.clicked.connect(self.view)
        self.l.addWidget(self.view_button)

        self.update_metadata_button = QPushButton(
            'Update metadata in a book\'s files', self)
#        self.update_metadata_button.clicked.connect(self.update_metadata)
        self.l.addWidget(self.update_metadata_button)

        self.conf_button = QPushButton(
                'Configure this plugin', self)
        self.conf_button.clicked.connect(self.config)
        self.l.addWidget(self.conf_button)

        self.resize(self.sizeHint())

    def about(self):
        # Get the about text from a file inside the plugin zip file
        # The get_resources function is a builtin function defined for all your
        # plugin code. It loads files from the plugin zip file. It returns
        # the bytes from the specified file.
        #
        # Note that if you are loading more than one file, for performance, you
        # should pass a list of names to get_resources. In this case,
        # get_resources will return a dictionary mapping names to bytes. Names that
        # are not found in the zip file will not be in the returned dictionary.
        text = get_resources('about.txt')
        QMessageBox.about(self, 'About the Tag Stats Plugin Prototype',
                text.decode('utf-8'))

    def tag_list_to_regexp(self, tag_list):
        ''' Convert a list of alternative globs to a single regexp. '''
        return re.compile("(?:" + string.join(map(fnmatch.translate, tag_list), ")|(?:") + ")")


    def increase_string_count(self, counter, string):
        ''' Add 1 to counter[string] (assuming missing value means 0). '''
        if string in counter:
            counter[string] = counter[string] + 1
        else:
            counter[string] = 1
    
    def add_tags_to_counter(self, counter, tags):
        ''' Add 1 to counter[tag] for every tag in tags '''
        if tags:
            for tag in tags:
                self.increase_string_count(counter, tag)
        
    def count_genres(self):
        ''' Count the genres and list the most common ones. '''

        genres = [
            {'label':"Science Fiction", 'tags':["science fiction*", "scifi*", "science-fiction*", "space*", "*other planet*", "sagas"]},
            {'label':"Fantasy",      	'tags':["fantasy*", "magic*"]},
            {'label':"Adventure",	'tags':["*adventure*"]},
            {'label':"Thriller",	'tags':["thriller*", "suspense*", "psychological*", "espionage*"]},
            {'label':"Mystery",		'tags':["mystery*", "*detective*", "*sleuth*", "murder*"]},
            {'label':"Romance",		'tags':["*romance*", "love*", "*romantic*"]},
            {'label':"Historical",	'tags':["*historical*"]},
            {'label':"Humour",		'tags':["*humour*", "*humorous*", "*parody*", "*satire*", "*satirical*"]},
            {'label':"Criminal",	'tags':["Criminal*", "Police*", "hard-boiled*"]},
            {'label':"Military",	'tags':["*military*", "*war*"]},
            {'label':"Erotica",		'tags':["*erotica*", "anal", "bdsm", "sex"]},
            {'label':"Religion",	'tags':["*religio*", "*christianity*", "*islam*", "*muslim*", "*buddhism*", "*hinduism*", "*catholi*", "*protestantism*"]},
            {'label':"Horror",		'tags':["*horror*", "*fear*", "*zombies*"]},
            {'label':"Classics",	'tags':["classics", "literature -classics"]},
            {'label':"Juvenile",	'tags':["*juvenile*", "*children's*"]},
            {'label':"Non Fiction",	'tags':["biography*", "*non fiction*", "*memoirs*", "*business*econom*", "travel", "computers*", "finance", "mathematics", "physics", "zoology", "programming*", "social science*", "political science*", "medical", "usenet", "reference*", "science", "*non-fiction*", "language arts*"]},
            ]

        locations = [
            {'label':"America", 'tags':["*america*", "*usa*", "*canad*", "*mexico*", "*brazil*", "*new york*", "NY", "*california*", "boston", "*los angeles*", "la", "*massachusetts*", "*texas*", "*north carolina*", "westerns", "*chicago*", "*florida*", "*maine*", "*alaska*", "n.y.", "seattle*", "new england", "new jersey", "*manhattan*", "*illinois*", "minnesota", "*new orleans*", "united states*", "montana", "las vegas*"]},
            {'label':"Europe",	'tags':["*europe*", "*sweden*", "*germany*", "*britain*", "*france*", "*italy*", "*ireland*", "*spain*", "*portugal*", "*poland*", "*russia*", "london", "rome", "english*", "*scotland*", "ireland", "england", "paris", "soviet*", "wales", "greece"]},
            {'label':"Africa",	'tags':["*africa*", "*egypt*"]},
            {'label':"Asia",	'tags':["*asia*", "*japan*", "*china*", "*hongkong*", "*singapore*", "*india*", "*iraq*", "*iran*", "*middle east*", "*far east*", "*vietnam*", "*pakistan*"]},
            {'label':"Oceania",	'tags':["*ocenania*", "*australia*", "*new zeeland*"]},
            ]

        over_generic_tags = ["fiction", "general", "literary", "fiction - general", "ebook", "book", "general & literary fiction", "essays", "general fiction"]

        for genre in genres:
            # Change globs to regexps.
            genre['tags'] = self.tag_list_to_regexp(genre['tags'])
            genre['count'] = 0
        
        for location in locations:
            # Change globs to regexps.
            location['tags'] = self.tag_list_to_regexp(location['tags'])
            location['count'] = 0
            
        tags_column_idx = self.db.FIELD_MAP['tags']
#        labels = ["Total", "Unknown", "Science Fiction", "Fantasy", "Adventure", "Thriller", "Mystery", "Romance"]
#        counts = [0, 0, 0, 0, 0, 0, 0, 0]; # Total, None/Other, Science Fiction, Fantasy, Adventure, Thriller, Mystery, Romance
        total_book_count = 0
        unknown_genre_book_count = 0
        unknown_location_book_count = 0
        common_tags_on_unknown_genre = {}
        common_tags_on_unknown_location = {}
        for record in self.db.data:
#        for record in self.db.data.iterall():
            # Iterate over all records
 #           # TODO - only iterate over the visible books.
            tags = record[tags_column_idx]
            total_book_count = total_book_count + 1
            known_genre_tag = False
            known_location_tag = False

            # This became much slower when going from "in string" matching to regexps. Too slow?
            book_tag_list = []
            if tags:
                book_tag_list = tags.lower().split(',')
                for genre in genres:
                    genre_tag_regexp = genre['tags']
                    for tag in book_tag_list:
                        if genre_tag_regexp.match(tag):
                            genre['count'] = genre['count'] + 1
                            known_genre_tag = True
                            break
                    
                for location in locations:
                    location_tag_regexp = location['tags']
                    for tag in book_tag_list:
                        if location_tag_regexp.match(tag):
                            location['count'] = location['count'] + 1
                            known_location_tag = True
                            break

            if not known_genre_tag:
                unknown_genre_book_count = unknown_genre_book_count + 1
                self.add_tags_to_counter(common_tags_on_unknown_genre, book_tag_list)

            if not known_location_tag:
                unknown_location_book_count = unknown_location_book_count + 1
                self.add_tags_to_counter(common_tags_on_unknown_location, book_tag_list)

        for over_generic_tag in over_generic_tags:
            if over_generic_tag in common_tags_on_unknown_genre:
                del common_tags_on_unknown_genre[over_generic_tag]
            if over_generic_tag in common_tags_on_unknown_location:
                del common_tags_on_unknown_location[over_generic_tag]

        common_strange_genre_tags = sorted(common_tags_on_unknown_genre.items(), key=itemgetter(1), reverse=True)
        print("\nCommon tags in books with unknown genre:")
        for i in range(20):
            (tag, count) = common_strange_genre_tags[i]
            print(str(i + 1) + ". " + tag + " (" + str(count) + ")")

        # The output from this just lists common genres. Meaningless.
        common_strange_location_tags = sorted(common_tags_on_unknown_location.items(), key=itemgetter(1), reverse=True)
        print("\nCommon tags in books with unknown location:")
        for i in range(20):
            (tag, count) = common_strange_location_tags[i]
            print(str(i + 1) + ". " + tag + " (" + str(count) + ")")
            
        results = []
        self.add_result_to_results(results, genres, unknown_genre_book_count, "Genre")
        self.add_result_to_results(results, locations, unknown_location_book_count, "Location")

        dialog = ChartDialog(self.gui, self.icon, total_book_count, results)
        dialog.show()

    def add_result_to_results(self, results, categories, unknown_count, title):
        category_results = []
        for category in categories:
            if category['count'] > 0:
                category_results.append((category['label'], category['count']))
        list.sort(category_results, key=itemgetter(1), reverse=True)
        if unknown_count > 0:
            category_results.append(("Unknown", unknown_count))
        results.append((title, category_results))

    def marked(self):
        ''' Show books with only one format '''
        fmt_idx = self.db.FIELD_MAP['formats']
        matched_ids = set()
        for record in self.db.data.iterall():
            # Iterate over all records
            fmts = record[fmt_idx]
            # fmts is either None or a comma separated list of formats
            if fmts and ',' not in fmts:
                matched_ids.add(record[0])
        # Mark the records with the matching ids
        self.db.set_marked_ids(matched_ids)

        # Tell the GUI to search for all marked records
        self.gui.search.setEditText('marked:true')
        self.gui.search.do_search()

    def view(self):
        ''' View the most recently added book '''
        most_recent = most_recent_id = None
        timestamp_idx = self.db.FIELD_MAP['timestamp']

        for record in self.db.data:
            # Iterate over all currently showing records
            timestamp = record[timestamp_idx]
            if most_recent is None or timestamp > most_recent:
                most_recent = timestamp
                most_recent_id = record[0]

        if most_recent_id is not None:
            # Get the row number of the id as shown in the GUI
            row_number = self.db.row(most_recent_id)
            # Get a reference to the View plugin
            view_plugin = self.gui.iactions['View']
            # Ask the view plugin to launch the viewer for row_number
            view_plugin._view_books([row_number])

    def update_metadata(self):
        '''
        Set the metadata in the files in the selected book's record to
        match the current metadata in the database.
        '''
        from calibre.ebooks.metadata.meta import set_metadata
        from calibre.gui2 import error_dialog, info_dialog

        # Get currently selected books
        rows = self.gui.library_view.selectionModel().selectedRows()
        if not rows or len(rows) == 0:
            return error_dialog(self.gui, 'Cannot update metadata',
                             'No books selected', show=True)
        # Map the rows to book ids
        ids = list(map(self.gui.library_view.model().id, rows))
        for book_id in ids:
            # Get the current metadata for this book from the db
            mi = self.db.get_metadata(book_id, index_is_id=True,
                    get_cover=True, cover_as_data=True)
            fmts = self.db.formats(book_id, index_is_id=True)
            if not fmts: continue
            for fmt in fmts.split(','):
                fmt = fmt.lower()
                # Get a python file object for the format. This will be either
                # an in memory file or a temporary on disk file
                ffile = self.db.format(book_id, fmt, index_is_id=True,
                        as_file=True)
                # Set metadata in the format
                set_metadata(ffile, mi, fmt)
                ffile.seek(0)
                # Now replace the file in the calibre library with the updated
                # file. We dont use add_format_with_hooks as the hooks were
                # already run when the file was first added to calibre.
                ffile.name = 'xxx' # add_format() will not work if the file
                                   # path of the file being added is the same
                                   # as the path of the file being replaced
                self.db.add_format(book_id, fmt, ffile, index_is_id=True)

        info_dialog(self, 'Updated files',
                'Updated the metadata in the files of %d book(s)'%len(ids),
                show=True)

    def config(self):
        self.do_user_config(parent=self)
        # Apply the changes
        self.label.setText(prefs['hello_world_msg'])

