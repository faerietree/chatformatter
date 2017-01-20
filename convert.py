#!/usr/bin/env python
# ========= CHAT FORMATTER =====================================================
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# ------- DESCRIPTION ----------------------------------------------------------
#
# """PURPOSE"""
# Format text dialog as whatsapp styled HTML.
#
#
# """WHAT IT DOES"""
# Take an input text file like the chat to email whatsapp export and format it.
#

# ------- LICENSING ------------------------------------------------------------
# Created by worlddevelopment, for an epic world (i@ciry.at)
# It's free, as is, open source and property to the World. But without warranty.
# Thus use it, improve it, recreate it and please at least keep the
# origin as in usual citation, i.e. include this Copyright note.
# LICENSE: creative commons, non-commercial, share-alike.
# Following this is advisable to not be hunted down by bots, machines and law fighters.
# ------------------------------------------------------------------------------




#------- IMPORTS --------------------------------------------------------------#
import chardet  # character encoding detection
import io
import os
import re
import sys
import time




#------- GLOBALS --------------------------------------------------------------#
# Show debug messages in blender console (that is the not python console!)
debug = True
chatMessages = []
chat_template_filepath = "chat.template.html"
chatMessages_count_per_file = 1000

in_f = sys.argv[1]
#out_f = sys.argv[2]
in_fn,in_ext = os.path.splitext(in_f)
#out_fn,out_ext = os.path.splitext(out_f)
print("Converting ", in_f, " to HTML chat output.")




#------- CLASSES --------------------------------------------------------------#
class ChatMessage():

    def __init__(self, attachments, author, text, time):
        self._author = author
        self._attachments = attachments
        #self._html = "" #html
        self._text = text
        self._time = time


    def getAttachments(self):
        return self._attachments

    def setAttachments(self, attachments):
        self._attachments = attachments
        return self

    def getAuthor(self):
        return self._author

    def setAuthor(self, author):
        self._author = author
        return self


    def getHtml(self):
        html = ('<li><div class="bubble">'
            '<span class="personName">' + self._author + '</span><br/>'
            '<span class="personSay">' + self._text + '</span>'
            '</div><span class="time round">'
            '<span class="arrow_left"></span>' + self._time + '<span class="arrow_right"></span></span><br/>'
            )
        for attachment in self._attachments:
            if attachment != "":
                html = html + '<a href="' + attachment + '">' + attachment + '</a>'#'<img src="' + attachment + '" alt=""/>'
        return html + '<p style="clear:both"></p></li>'


    def getText(self):
        return self._text

    def setText(self, text):
        self._text = text
        return self

    def appendText(self, text):
        self._text += text
        return self


    def getTime(self):
        return self._time

    def setTime(self, time):
        self._time = time
        return self




#------- FUNCTIONS ------------------------------------------------------------#
#
# Guarantuee a valid initial state.
#
def init():
    global chatMessages
    chatMessages = []



def debug(message):
    if debug:
        print(message)


def build_filelink(file_counter):
    return in_f + "." + str(file_counter) + ".html"


#
# ACT
#
def main():
    global bom_entry_count_map

    init()

    debug('Engine started ... (acting according to setting)')

    read_file()

    dialog_html = ""
    chatMessages_index = 1
    file_counter = 0
    chatMessage_author_previous = ""
    while chatMessages_index < len(chatMessages):
        chatMessage = chatMessages[chatMessages_index]
        # Keep the same author on the same side throughout the dialog, the side is set via CSS nth-of-type(2n+1):
        if chatMessage_author_previous != chatMessage.getAuthor():
            chatMessage_author_previous = chatMessage.getAuthor()
            #debug("chatMessage_author_previous:" + chatMessage_author_previous)
            dialog_html = dialog_html + "\r\n" + chatMessage.getHtml()
        else:
            dialog_html = dialog_html + "\r\n<li></li>" + chatMessage.getHtml()

        # Create a new file every X entries:
        if chatMessages_index % chatMessages_count_per_file == 0:
            file_counter = write_to_file(dialog_html, file_counter)
            dialog_html = ""
        chatMessages_index += 1
        #debugreturn False

    if dialog_html != "":
        write_to_file(dialog_html, file_counter)

    #Everything was fine then!
    return True

    ############
    #act-furthermore
    ############
    # a smiley :) highly underestimated



#
#
#
def write_to_file(dialog_html, file_counter):
    html = ""
    print("Reading file: ", chat_template_filepath)
    filelink = build_filelink(file_counter)
    print("Writing to file: ", filelink)
    file_counter += 1
    dialog_html += '<li><div class="next"><a href="../' + build_filelink(file_counter) + '" alt="">Next: ' + str(file_counter) + '</a></div></li>'
    with io.open(chat_template_filepath, 'r', encoding='utf8') as f:
        for line in f:
            if line.find('%dialog%') != -1:
                html = html + "\r\n" + dialog_html + "\r\n"
            elif line.find('%encoding%') != -1:
                html = html + "\r\n" + line.replace('%encoding%', encoding)
            else:
                html = html + line
    write_file(html, filelink)
    return file_counter



#
#
#
def read_file():
    global chatMessages
    global encoding
    print("Opening file: ", in_f)
    detection = chardet.detect(open(in_f, 'rb').read())  # TODO Read big file as chunks into memory instead of all at once.
    encoding = detection["encoding"]
    debug(str(detection) + " => " + encoding)
    #encoding = 'ANSI_X3.4-1968'
    #encoding = 'utf-8'
    chatMessage_previous = ""
    with io.open(in_f, 'r', encoding=encoding) as f:
    #with io.open(in_f, 'rb', encoding=encoding) as f:
        for line in f:
        #for line_ in f.readlines():
            #line = line_.decode(encoding)
            #line_ = line_.encode('utf-8')
            #line = line_.decode('utf-8')
            #debug("line type: " + str(type(line)))
            #debug("line_ type: " + str(type(line_)))
            debug(line.encode('utf-8'))  # terminal not supports the other encoding
            parts = line.split(' - ')
            if len(parts) > 1:
                if chatMessage_previous:
                    chatMessages.append(chatMessage_previous)
                    del chatMessage_previous
                time = parts[0].strip()  # remove leading, trailing white space
                parts = parts[1].split(":")
                author = parts[0].strip()
                #parts = parts[1].split(" ")
                text = parts[1]
                attachments = []
                if text.find(" (Datei") != -1 or text.find(" (File") != -1:
                    text = "Attached file(s)."
                    attachments = re.sub("\(File.*\)", "", re.sub("\(Datei.*\)", "", parts[1])).strip().split(";")
                chatMessage_previous = ChatMessage(attachments, author, text, time)
            else:
                if chatMessage_previous:
                    chatMessage_previous.appendText("\r\n<br/>" + line)
                else:
                    print("Message starts without author, time, et alia meta data: ", line)
        # Store the last chat message:
        if chatMessage_previous:
            chatMessages.append(chatMessage_previous)
            del chatMessage_previous


#
#
#
def write_file(html, filepath):
    print("Exporting to file: ", filepath)
    if filepath == chat_template_filepath:
        print("Export to %s aborted because the output filepath is equal to the template filepath." % filepath)
    elif filepath == in_f:
        print("Export to %s aborted because the output filepath is equal to the input filepath." % filepath)
    else:
        with io.open(filepath, 'w', encoding=encoding) as f:
            f.write(html)
            print("Exported to '%s'." % (filepath))


# Allow importing the script without running it:
if __name__ == '__main__':
   main()


