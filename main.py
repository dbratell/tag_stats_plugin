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
from datetime import datetime
from calibre.utils.date import UNDEFINED_DATE

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
            'Count genres, locations and publication years', self)
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


    def increase_number_count(self, counter, number):
        ''' Add 1 to counter[number] (assuming missing value means 0). '''
        if number in counter:
            counter[number] = counter[number] + 1
        else:
            counter[number] = 1
    
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
        else:
            self.increase_string_count(counter, "No tag at all")
        
    def count_genres(self):
        ''' Count the genres and list the most common ones. '''

        genres = [
            {'label':"Science Fiction", 'tags':["science fiction*", "scifi*", "science-fiction*", "space*", "*other planet*", "sagas"]},
            {'label':"Fantasy",      	'tags':["fantasy*", "magic*"]},
            {'label':"Adventure",	'tags':["*adventure*", "*pirates*"]},
            {'label':"Thriller",	'tags':["*thriller*", "suspense*", "psychological*", "espionage*"]},
            {'label':"Mystery",		'tags':["mystery*", "*detective*", "*sleuth*", "murder*"]},
            {'label':"Romance",		'tags':["*romance*", "love*", "*romantic*"]},
            {'label':"Historical",	'tags':["*historical*"]},
            {'label':"Humour",		'tags':["*humour*", "*humorous*", "*parody*", "*satire*", "*satirical*", "humor*"]},
            {'label':"Criminal",	'tags':["Criminal*", "Police*", "hard-boiled*", "crime"]},
            {'label':"Military",	'tags':["*military*", "*war*"]},
            {'label':"Erotica",		'tags':["*erotica*", "anal", "bdsm", "sex"]},
            {'label':"Religion",	'tags':["*religio*", "*christianity*", "*islam*", "*muslim*", "*buddhism*", "*hinduism*", "*catholi*", "*protestantism*"]},
            {'label':"Horror",		'tags':["*horror*", "*fear*", "*zombies*"]},
            {'label':"Classics",	'tags':["classics", "literature -classics"]},
            {'label':"Juvenile",	'tags':["*juvenile*", "*children's*"]},
            {'label':"Non Fiction",	'tags':["biography*", "*non fiction*", "*memoirs*", "*business*econom*", "travel", "computers*", "finance", "mathematics", "physics", "zoology", "programming*", "social science*", "political science*", "medical", "usenet", "reference*", "science", "*non-fiction*", "language arts*", "philosophy", "*edcuation*", "*nonfiction*"]},
            ]

        locations = [
            {'label':"America", 'tags':["*america*", "*usa*", "*canad*", "*mexico*", "*brazil*", "*new york*", "NY", "*california*", "boston", "*los angeles*", "la", "*massachusetts*", "*texas*", "*north carolina*", "westerns", "*chicago*", "*florida*", "*maine*", "*alaska*", "n.y.", "seattle*", "new england", "new jersey", "*manhattan*", "*illinois*", "minnesota", "*new orleans*", "united states*", "montana", "las vegas*"]},
            {'label':"Europe",	'tags':["*europe*", "*sweden*", "*germany*", "*britain*", "*france*", "*italy*", "*ireland*", "*spain*", "*portugal*", "*poland*", "*russia*", "london", "rome", "english*", "*scotland*", "ireland", "england", "paris", "soviet*", "wales", "greece", "*(wales)"]},
            {'label':"Africa",	'tags':["*africa*", "*egypt*"]},
            {'label':"Asia",	'tags':["*asia*", "*japan*", "*china*", "*hongkong*", "*singapore*", "*india*", "*iraq*", "*iran*", "*middle east*", "*far east*", "*vietnam*", "*pakistan*"]},
            {'label':"Oceania",	'tags':["*ocenania*", "*australia*", "*new zeeland*"]},
            ]

        over_generic_tags = ["fiction", "general", "literary", "fiction - general", "ebook", "book", "general & literary fiction", "essays", "general fiction", "fiction & literature", "popular literature"]

        for genre in genres:
            # Change globs to regexps.
            genre['tags'] = self.tag_list_to_regexp(genre['tags'])
            genre['count'] = 0
        
        for location in locations:
            # Change globs to regexps.
            location['tags'] = self.tag_list_to_regexp(location['tags'])
            location['count'] = 0
            
        tags_column_idx = self.db.FIELD_MAP['tags']
        pubdate_column_idx = self.db.FIELD_MAP['pubdate']
        title_column_idx = self.db.FIELD_MAP['title']
        rating_column_idx = self.db.FIELD_MAP['rating']
        format_column_idx = self.db.FIELD_MAP['formats']
        
#        labels = ["Total", "Unknown", "Science Fiction", "Fantasy", "Adventure", "Thriller", "Mystery", "Romance"]
#        counts = [0, 0, 0, 0, 0, 0, 0, 0]; # Total, None/Other, Science Fiction, Fantasy, Adventure, Thriller, Mystery, Romance
        total_book_count = 0
        unknown_genre_book_count = 0
        unknown_location_book_count = 0
        common_tags_on_unknown_genre = {}
        common_tags_on_unknown_location = {}
        year_histogram = {}
        rating_integer_histogram = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 }
        rating_exact_histogram = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0 }
        unknown_year_book_count = 0
        title_word_counter = {}
        format_count_histogram = {}
        format_counter = {}
        
        for record in self.db.data:
#        for record in self.db.data.iterall(): # This would iterate over all books in the database.
            # Iterate over visible books.
            book_title = record[title_column_idx]
            tags = record[tags_column_idx]
            total_book_count = total_book_count + 1
            known_genre_tag = False
            known_location_tag = False

            book_words = set()
            for book_word in book_title.lower().split():
                book_word = string.strip(book_word, ":&-()")
                if book_word:
                    book_words.add(book_word)

            for book_word in book_words:
                self.increase_string_count(title_word_counter, book_word)
            
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


            pubdate_datetime = record[pubdate_column_idx]
#                pubdate_datetime = datetime.strptime(pubdate, "%Y-%m-%dT%H:%M:%s%z")
#                print(str(pubdate_datetime))
            # The handling of UNDEFINED_DATE has timezone troubles...
            if pubdate_datetime.date() != UNDEFINED_DATE.date():
                year = pubdate_datetime.year
                if year < 1000:
                    print("Bad pubdate (" + str(pubdate_datetime) + ") for book " + book_title + " by " + str(record[self.db.FIELD_MAP['authors']]))
                    print("UNDEFINED_DATE = " + str(UNDEFINED_DATE))
                self.increase_number_count(year_histogram, year)
            else:
                unknown_year_book_count = unknown_year_book_count + 1

            rating = record[rating_column_idx]
            if rating:
                int_rating = int(rating / 2)
                rating_integer_histogram[int_rating] = rating_integer_histogram[int_rating] + 1
                rating_exact_histogram[rating] = rating_exact_histogram[rating] + 1

            formats = record[format_column_idx]
            format_count = 0
            if formats:
                format_list = formats.split(',')
                format_count = len(format_list)
                for format in format_list:
                    self.increase_number_count(format_counter, format)
            self.increase_number_count(format_count_histogram, format_count)
            
            
        for over_generic_tag in over_generic_tags:
            if over_generic_tag in common_tags_on_unknown_genre:
                del common_tags_on_unknown_genre[over_generic_tag]
            if over_generic_tag in common_tags_on_unknown_location:
                del common_tags_on_unknown_location[over_generic_tag]

        common_strange_genre_tags = sorted(common_tags_on_unknown_genre.items(), key=itemgetter(1), reverse=True)
        print("\nCommon tags in books with unknown genre:")
        for i in range(min(20, len(common_strange_genre_tags))):
            (tag, count) = common_strange_genre_tags[i]
            print(str(i + 1) + ". " + tag + " (" + str(count) + ")")

        # The output from this just lists common genres. Meaningless.
        # common_strange_location_tags = sorted(common_tags_on_unknown_location.items(), key=itemgetter(1), reverse=True)
        # print("\nCommon tags in books with unknown location:")
        # for i in range(min(20, len(common_strange_location_tags))):
        #     (tag, count) = common_strange_location_tags[i]
        #     print(str(i + 1) + ". " + tag + " (" + str(count) + ")")

        over_generic_book_title_words = ["the", "a", "of", "at", "in", "to", "on", "and", "for", "an", "from", "&", "-", "with", "is", "are", "was", "by"]
        for over_generic_book_title_word in over_generic_book_title_words:
            if over_generic_book_title_word in title_word_counter:
                del title_word_counter[over_generic_book_title_word]

        top_list_max_length = 20
        common_title_words = sorted(title_word_counter.items(), key=itemgetter(1), reverse=True)[:top_list_max_length]
        print("\nCommon title words:")
        common_word_pos = 1
        for (common_title_word, common_title_word_count) in common_title_words:
            print(str(common_word_pos) + ". " + common_title_word + " (" + str(common_title_word_count) + ")")
            common_word_pos = common_word_pos + 1
                
        # for year in sorted(year_histogram.keys()):
        #     print(str(year) + " - " + str(year_histogram[year]))
            
        results = []
        self.add_result_to_results(results, genres, unknown_genre_book_count, total_book_count, "Genre")
        self.add_histogram_to_results(results, year_histogram, unknown_year_book_count, "Books per year")
        self.add_histogram_to_results(results, rating_integer_histogram, 0, "Ratings")
        self.add_histogram_to_results(results, rating_exact_histogram, 0, "Exact ratings")
        self.add_result_to_results(results, locations, unknown_location_book_count, total_book_count, "Location")
        self.add_top_list_to_results(results, common_title_words, "Common title words")
        self.add_counter_to_results(results, format_counter.items(), total_book_count, "Formats")
        self.add_histogram_to_results(results, format_count_histogram, 0, "Formats/book")
        
        dialog = ChartDialog(self.gui, self.icon, results)
        dialog.show()

    def add_histogram_to_results(self, results, histogram, unknown_count, title):
        ''' Take a histogram (mapping from sample number to count) and insert
        a result block (title, bars, scale) in results. '''
        histogram_results = []
        histogram_max_value = 1
        if histogram:
            for sample in range(min(histogram.keys()), max(histogram.keys()) + 1):
                count_for_sample = 0
                if (sample in histogram):
                    count_for_sample = histogram[sample]
                    histogram_max_value = max(histogram_max_value, histogram[sample])
                histogram_results.append((str(sample), count_for_sample))
        if unknown_count > 0:
            histogram_results.append(("Unknown", unknown_count))
            histogram_max_value = max(histogram_max_value, unknown_count)
        results.append(("histogram", title, histogram_results, histogram_max_value))

        
    def add_counter_to_results(self, results, counter, max_value, title):
        counter_results = []
        for (label, count) in counter:
            counter_results.append((label, count))
        list.sort(counter_results, key=itemgetter(1), reverse=True)
        results.append(("bar", title, counter_results, max_value))

    def add_result_to_results(self, results, categories, unknown_count, max_value, title):
        category_results = []
        for category in categories:
            if category['count'] > 0:
                category_results.append((category['label'], category['count']))
        list.sort(category_results, key=itemgetter(1), reverse=True)
        if unknown_count > 0:
            category_results.append(("Unknown", unknown_count))
        results.append(("bar", title, category_results, max_value))

    def add_top_list_to_results(self, results, top_list, title):
        ''' top_list needs to be pre-sorted and pre-truncated '''
        top_list_results = []
        for (label, value) in top_list:
            top_list_results.append((label, value))
        results.append(("list", title, top_list_results))

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

