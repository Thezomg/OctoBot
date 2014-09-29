def get_type(command, args=None):
    typ = {
        '001': lambda x: "rpl_welcome",      # first message sent after registration
        '002': lambda x: "rpl_yourhost",     # Part of post-registration greeting
        '003': lambda x: "rpl_created",      # Part of post-registration greeting
        '004': lambda x: "rpl_myinfo",       # Part of post-registration greeting
        #'005': lambda x: "rpl_bounce",      # Try additional server if full
        '005': lambda x: "rpl_isupport",     # Stuff the server supports (not required)
        # From: http://www.irc.org/tech_docs/005.html
        # PREFIX - List of Channel Modes Supported, eg: PREFIX=(ov)@+
        # CHANTYPES - List of channel prefixes, eg: CHANTYPES=#&
        # CHANMODES - List of channel modes, eg: CHANMODES=b,k,l,imnpstr
        #   CHANMODES Comes in as A,B,C,D
        #   A = Mode that adds or removes a nick/address to a list (requires parameter)
        #   B = Mode that changes a setting (eg: password on the channel) (requires parameter)
        #   C = Mode that changes a setting, only has a parameter for adding
        #   D = Mode that changes a setting, never has a parameter
        # MODES - Maximum number of channel modes with paramter allowed per mode command
        # MAXCHANNELS - Max channels allowed to join, eg: MAXCHANNELS=3, replaced by CHANLIMIT
        # CHANLIMIT - Max channels allowed to join based on prefix, eg: PREFIX=#&!+:10
        # NICKLEN - Max nick length, eg: NICKLEN=9
        # MAXBANS - Maximum number of bans on a channel, eg: MAXBANS=30, replaced by MAXLIST
        # MAXLIST - Maximum number per list by mode (mode:num[,mode:num]...), eg: MAXLIST=beI:30
        # NETWORK - Network name, eg: NETWORK=GameSurge
        # EXCEPTS - The server support ban exceptions, eg: EXCEPTS=e
        # INVEX - The server supports invite exceptions, eg: INVEX=I
        # WALLCHOPS - The server supports messaging channel operators, eg: WALLCHOPS
        # WALLVOICES - The server supports messaging all channel +v, eg: WALLVOICES
        # STATUSMSG - The server supports messages channel member who have status or higher, eg: STATUSMSG=+@
        # CASEMAPPING - Case mapping used for nick and channel name comparing, eg: CASEMAPPING=rfc1459
        # ELIST - Server supports extensions for the LIST command, eg: ELIST=U
        #   M = mask search
        #   N = !mask search
        #   U = user count search (< >)
        #   C = creation time search (C<  C>)
        #   T = Topic search (T<  T>)
        # TOPICLEN - The length allowed for topics, eg: TOPICLEN=80
        # KICKLEN - The length allowed for kick messages, eg: KICKLEN=50
        # CHANNELLEN - The length allowed for channel names, eg: CHANNELLEN=50
        # CHIDLEN - The ID length for !channels (5 by default), eg: CHIDLEN=5, replaced by IDCHAN
        # IDCHAN - The ID length for channels with an ID, eg: IDCHAN=!:5
        '006': lambda x: "rpl_map",          # Unreal
        '007': lambda x: "rpl_mapend",       # Unreal
        '008': lambda x: "rpl_snomask",      # server notice mask
        '009': lambda x: "rpl_statmenot",
        '010': lambda x: "rpl_bounce",       # Redirect to another server
        '014': lambda x: "rpl_yourcookie",
        '015': lambda x: "rpl_map",
        '016': lambda x: "rpl_mapmode",
        '017': lambda x: "rpl_mapend",
        '042': lambda x: "rpl_yourid",
        '043': lambda x: "rpl_savenick",     # Send to the client when forced to change nick
        '050': lambda x: "rpl_attemptingjunc",
        '051': lambda x: "rpl_attemptingroute",
        '200': lambda x: "rpl_tracelink",
        '201': lambda x: "rpl_traceconnecting",
        '202': lambda x: "rpl_tracehandshake",
        '203': lambda x: "rpl_traceunknown",
        '204': lambda x: "rpl_traceoperator",
        '205': lambda x: "rpl_traceuser",
        '206': lambda x: "rpl_traceserver",
        '207': lambda x: "rpl_traceservice",
        '208': lambda x: "rpl_tracenewtype",
        '209': lambda x: "rpl_traceclass",
        # Need to determine which type it is.
        #'210': lambda x: "rpl_tracereconnect",
        #'210': lambda x: "rpl_stats",
        '211': lambda x: "rpl_statslinkinfo", 
        '212': lambda x: "rpl_statscommands",
        '213': lambda x: "rpl_statscline",
        '214': lambda x: "rpl_statsnline",
        '215': lambda x: "rpl_statsiline",
        '216': lambda x: "rpl_statskline",
        # determine difference here
        #'217': lambda x: "rpl_statsqline",
        #'217': lambda x: "rpl_statspline",
        '218': lambda x: "rpl_statsyline",
        '219': lambda x: "rpl_endofstats",
        # determine difference here
        #'220': lambda x: "rpl_statspline",
        #'220': lambda x: "rpl_statsbline",
        '221': lambda x: "rpl_umodeis", # <user_modes> [user_mode_params]
        '231': lambda x: "rpl_serviceinfo",
        '232': lambda x: "rpl_endofservices",
        '233': lambda x: "rpl_serivce",
        '234': lambda x: "rpl_servlist",     # <name> <server> <mask> <type> <hopcount> <info>
        '235': lambda x: "rpl_servlistend",  # <mask> <type> :<info>
        '241': lambda x: "rpl_statslline",   # L <hostmask> * <servername> <maxdepth>
        '242': lambda x: "rpl_statsuptime",  # :Server Up <days> days <hours>:<minutes>:<seconds>
        '243': lambda x: "rpl_statsoline",   # O <hostmask> * <nick> [:<info>]
        '244': lambda x: "rpl_statshline",   # H <hostname> * <servername>
        '246': lambda x: "rpl_statsping",
        '247': lambda x: "rpl_statsbline",
        '250': lambda x: "rpl_statsconn",
        '251': lambda x: "rpl_luserclient",  # :There are <int> users and <int> invisible on <int> servers (text may differ)
        '252': lambda x: "rpl_luserop",      # <int> :<info>
        '253': lambda x: "rpl_luserunknown", # <int> :<info>
        '254': lambda x: "rpl_luserchannels",# <int> :<info>
        '255': lambda x: "rpl_luserme",      # :I have <int> clients and <int> servers
        '256': lambda x: "rpl_adminme",      # [<server> ]:<info>
        '257': lambda x: "rpl_adminloc1",    # :<location>
        '258': lambda x: "rpl_adminloc2",    # :<location>
        '259': lambda x: "rpl_adminemail",   # :<email>
        '261': lambda x: "rpl_tracelog",     # File <logfile> <debug_level>
        # code function for difference
        #'262': lambda x: "rpl_tracelog",
        #'262': lambda x: "rpl_tracelog",     # <server_name> <version>[ . <debug_level>] :<info>
        '263': lambda x: "rpl_tryagain",     # If server drops command, must send this. <command>: <info>
        '265': lambda x: "rpl_localusers",
        '266': lambda x: "rpl_globalusers",
        '300': lambda x: "rpl_none",         # Shouldn't see this, used for testing
        '301': lambda x: "rpl_away",         # Users in reply to a command directed at an away user. <nick>[ <seconds away>] :<message>
        '302': lambda x: "rpl_userhost",     # :*1<reply> *( ' ' <reply> )
        '303': lambda x: "rpl_ison",         # :*1<user> *( ' ' <nick> )
        '304': lambda x: "rpl_text",
        '305': lambda x: "rpl_unaway",       # Reply from away when no longer away.  :<info>
        '306': lambda x: "rpl_nowaway",      # Reply from away when now away.  :<info>

        ## who/whois/whowas replies

        '311': lambda x: "rpl_whoisuser",    # <nick> <user> <host> * :<realname>    Reply to whois 
        '312': lambda x: "rpl_whoisserver",  # <nick> <server> :<server_info>        Reply to whois
        '313': lambda x: "rpl_whoisoperator",# <nick> :<privileges>                  Reply to whois
        '314': lambda x: "rpl_whowasuser",   # <nick> <user> <host> * :<realname>    Reply to whowas
        '315': lambda x: "rpl_endofwho",     # <name> :<info>                        Reply to who
        '316': lambda x: "rpl_whoischanop",
        '317': lambda x: "rpl_whoisidle",    # <nick> <seconds> :seconds idle        Reply to whois
        '318': lambda x: "rpl_endofwhois",   # <nick> :<info>                        Reply to whois
        '319': lambda x: "rpl_whoischannels",# <nick> :&( ( '@' / '+' )<channel>' ') Reply to whois
        #'320': lambda x: "rpl_whoisvert",
        #'320': lambda x: "rpl_whois_hidden",
        #'320': lambda x: "rpl_whoisspecial",

        # code functions for difference 
        '330': lambda x: "rpl_whowas_time",
        '330': lambda x: "rpl_whoisaccount", # <nick> <authname> :<info>

        ###

        '321': lambda x:"rpl_liststart",    # Channels: Users Name
        '322': lambda x:"rpl_list",         # <channel> <# visible> :<topic>
        '323': lambda x:"rpl_listend",      # :<info>
        '324': lambda x:"rpl_channelmodeis",# <channel> <mode> <mode_params>

        # code function for difference
        #'325': lambda x:"rpl_uniqpis",      # <channe> <nickname> RFC2812
        #'325': lambda x:"rpl_channelpassis",

        '326': lambda x:"rpl_nochanpass",
        '327': lambda x:"rpl_chpassunknown",
        '328': lambda x:"rpl_channel_url",
        '329': lambda x:"rpl_creationtime",

        '331': lambda x:"rpl_notopic",      # <channel> :<info>
        '332': lambda x:"rpl_topic",        # <channel> :<topic>
        '333': lambda x:"rpl_topicwhotime",
        '339': lambda x:"rpl_badchanpass",
        '340': lambda x:"rpl_userid",
        '341': lambda x:"rpl_inviting",     # <nick> <channel>  When invite sent successfully to user
        '342': lambda x:"rpl_summoning",    # <user> :<info>    Returned by a server to SUMMON on user
        '345': lambda x:"rpl_invited",      # <channel> <user invited> <user inviting> :<user invited> has been invited by <user inviting>  Sent to users on a channel when a user have been invited
        '346': lambda x:"rpl_invitelist",   # <channe> <invite mask>
        '347': lambda x:"rpl_endofinvitelist", # <channel> :<info>
        '348': lambda x:"rpl_exceptlist",   # <channel> <exception mask>
        '349': lambda x:"rpl_endofexceptlist", # <channel> :<info>
        '351': lambda x:"rpl_version",      # <version>[. <debuglevel>] <server> :<comments> 
        '352': lambda x:"rpl_whoreply",     # <channel> <user> <host> <server> <nick> <H|G>[*][@|+] :<hopcount> <real_name>
        '353': lambda x:"rpl_namreply",     # ( '=' / '*' / '@' ) <channel> ' ' : [ '@' / '+' ] <nick> *( ' ' [ '@' / '+' ] <nick> )
        '354': lambda x:"rpl_whospcrpl",
        '355': lambda x:"rpl_namreply_",    # ( '=' / '*' / '@' ) <channel> ' ' : [ '@' / '+' ] <nick> *( ' ' [ '@' / '+' ] <nick> )  NAMES -d
        '364': lambda x:"rpl_links",        # <mask> <server> :<hopcount> <server_info>
        '365': lambda x:"rpl_endoflinks",   # <mask> :<info>
        '366': lambda x:"rpl_endofnames",   # <channel> :<info>
        '367': lambda x:"rpl_banlist",      # <channel> <banid> [<time_left] :<reason>]
        '368': lambda x:"rpl_endofbanlist", # <channel> :<info>
        '369': lambda x:"rpl_endofwhowas",  # <nick> :<info>
        '371': lambda x:"rpl_info",         # :<string>
        '372': lambda x:"rpl_motd",         # :- <string>
        '373': lambda x:"rpl_infostart",
        '374': lambda x:"rpl_endofinfo",
        '375': lambda x:"rpl_motdstart",    # :- <server> Message of the day -
        '376': lambda x:"rpl_endofmotd",    # :<info>
        '377': lambda x:"rpl_spam",         # :<info>
        '378': lambda x:"rpl_motd",         # :- <string>
        '381': lambda x:"rpl_youreoper",    # :<info>  successful OPER call
        '382': lambda x:"rpl_rehashing",    # <config_file> :<info>  sucessful REHASH call
        '383': lambda x:"rpl_youreservice", # :You are service <service name>
        '384': lambda x:"rpl_myportis",
        '385': lambda x:"rpl_notoperanymore",
        '388': lambda x:"rpl_alist",
        '389': lambda x:"rpl_endofalist",
        '391': lambda x:"rpl_time",         # TIME reply, multiple reply options
        # <server> :<time string>
        # <server> <timestamp> <offset> :<time string>
        # <server> <timezone name> <microseconds> :<time string>
        # <server> <year> <month> <day> <hour> <minute> <second> - Supposedly relative to UTC
        '392': lambda x:"rpl_usersstart",   # :UserID Terminal Host
        '393': lambda x:"rpl_users",        # :<username> <ttyline> <hostname>
        '394': lambda x:"rpl_endofusers",   # :<info>
        '395': lambda x:"rpl_nousers",      # :<info>
        '396': lambda x:"rpl_hosthidden",

        '400': lambda x:"err_unknownerror", # :<command [<?>] :<info>
        '401': lambda x:"err_nosuchnick",   # <nick> :<reason>
        '402': lambda x:"err_nosuchserver", # <server> :<reason>
        '403': lambda x:"err_nosuchchannel",# <channel> :<reason>
        '404': lambda x:"err_cannotsendtochan",# <channel> :<reason>
        '405': lambda x:"err_toomanychannels",# <channel> :<reason>
        '406': lambda x:"err_wasnosuchnick",# <nick> :<reason>
        '407': lambda x:"err_toomanytargets",# <target> :<reason>
        '408': lambda x:"err_nosuchservice",# <service> :<reason>
        #'408': lambda x:"err_nocolorsonchan",
        '409': lambda x:"err_nosuchorigin", # :<reason>
        '411': lambda x:"err_norecipient",  # :<reason>
        '412': lambda x:"err_notexttosend", # :<reason>
        '413': lambda x:"err_notoplevel",   # <mask> :<reason>   notice without TLD (eg: * instead of *.au)
        '414': lambda x:"err_wildtoplevel", # <mask> :<reason>   notice with wild TLD (eg: *.*)
        '415': lambda x:"err_badmask",      # <mask> :<reason>
        '416': lambda x:"err_toomanymatches",# <command> <mask> :<reason>   when a command wouldtoo many matches eg: /who *
        '419': lambda x:"err_lengthtruncated",
        '421': lambda x:"err_unknowncommand",# <command> :<reason>
        '422': lambda x:"err_nomotd",       # :<reason>
        '423': lambda x:"err_noadmininfo",  # <server> :<reason>
        '424': lambda x:"err_fileerror",    # :<reason>
        '425': lambda x:"err_noopermotd",
        '429': lambda x:"err_toomanyaway",
        '430': lambda x:"err_eventnickchange",# returned by nick if user not allowed to change due to channel event (eg: mode +E)
        '431': lambda x:"err_nonicknamegiven",# :<reason>    expected nickname but didn't get it.
        '432': lambda x:"err_erroneusnickname",# <nick> :<reason>    trying to use reserved or invalid nickname
        '433': lambda x:"err_nicknameinuse",# <nick> :<reason>    nickname already in use
        '436': lambda x:"err_nickcollision",# <nick> :<reason>    nickname collision
        '439': lambda x:"err_targettooface",
        '440': lambda x:"err_servicesdown",
        '441': lambda x:"err_usernotinchannel",# <nick> <channel> :<reason>     nick not in channel
        '442': lambda x:"err_notinchannel", # <channel> :<reason>       trying to do thing in channel when not a member
        '443': lambda x:"err_useronchannel",# <nick> <channel> [:<reason>]    when trying to invite user to channel when they are there.
        '444': lambda x:"err_nologin",      # <user> :<reason>    user not logged in and can't be SUMMONED
        '445': lambda x:"err_summondisabled",# :<reason>
        '446': lambda x:"err_usersdisabled",# :<reason>
        '447': lambda x:"err_nonickchange",
        '449': lambda x:"err_notimplemented",
        '451': lambda x:"err_notregistered",# :<reason>
        '452': lambda x:"err_idcollision",
        '453': lambda x:"err_nicklost",
        '455': lambda x:"err_hostilename",
        '456': lambda x:"err_acceptfull",
        '457': lambda x:"err_acceptexist",
        '458': lambda x:"err_acceptnot",
        '459': lambda x:"err_nohiding",
        '460': lambda x:"err_notforhalfops",
        '461': lambda x:"err_needmoreparams",# <command> :<reason>
        '462': lambda x:"err_alreadyregistered",# :<reason>
        '463': lambda x:"err_noperformhost",# :<reason>    returned by server told not to accept from host
        '464': lambda x:"err_passwdmismatch",# :<reason>   password doesn't match
        '465': lambda x:"err_yourebannedcreep",# :<reason>     when trying to register and client host banned
        '466': lambda x:"err_youwillbebanned",
        '467': lambda x:"err_keyset",       # <channel> :<reason>   channel key already set
        '469': lambda x:"err_linkset",
        '471': lambda x:"err_channelisfull",# <channe> :<reason>     when channel it full
        '472': lambda x:"err_unknownmode",  # <char> :<reason>          when trying to set and unknown mode
        '473': lambda x:"err_inviteonlychan",# <channel> :<reason>      when trying to join channel that is invite only
        '474': lambda x:"err_bannedfromchan",# <channel> :<reason>      when trying to join channel when banned
        '475': lambda x:"err_banchannelkey",# <channel> :<reason>       when trying to join channel with incorrect key
        '476': lambda x:"err_banchanmask",  # <channel> :<reason>       given channel mask was invalid
        '477': lambda x:"err_nochanmodes",  # <channel> :<reason>       when trying to set/change mode on modeless channel
        '478': lambda x:"err_banlistfull",  # <channel> <char> :<reason> ban list is full and can't be added to
        #'479': lambda x:"err_badchanname",
        #'479': lambda x:"err_linkfail",
        '481': lambda x:"err_noprivileges", # :<reason>   returned by any command requiring special privileges
        '482': lambda x:"err_chanprivsneeded",# <channel> :<reason>   special privileges required in channel to run command
        '483': lambda x:"err_cantkillserver",# :<reason>
        '484': lambda x:"err_restricted",   # :<reason>
        '485': lambda x:"err_uniqprivsneeded",# :<reason>   and mode requiring channel creator privileges
        '488': lambda x:"err_tslesschan",
        '491': lambda x:"err_nooperhost",   # :<reason>  by oper to a client because denied for client's host
        '492': lambda x:"err_noservicehost",
        '493': lambda x:"err_nofeature",
        '494': lambda x:"err_badfeature",
        '495': lambda x:"err_badlogtype",
        '496': lambda x:"err_badlogsys",
        '497': lambda x:"err_badlogvalue",
        '498': lambda x:"err_isoperlchan",
        '499': lambda x:"err_chanownprivneeded",#       +q needed on channel
        '501': lambda x:"err_umodeunknownflag", # :<reason>      unrecognized umode
        '502': lambda x:"err_usersdontmatch",   # :<reason>      trying to see another users modes
        '503': lambda x:"err_ghostedclient",
        '504': lambda x:"err_usernotonserv",
        '511': lambda x:"err_silelistfull",
        '512': lambda x:"err_toomanywatch",
        '513': lambda x:"err_badping",
        '515': lambda x:"err_badexpire",
        '516': lambda x:"err_dontcheat",
        '517': lambda x:"err_disabled",         # <command> :<info/reason>
        '522': lambda x:"err_whosyntax",
        '523': lambda x:"err_wholimexceeded",
        '550': lambda x:"err_badhostmask",
        '551': lambda x:"err_hostunavail",
        '552': lambda x:"err_usingsline",

        ## The rest really aren't RFC, can be added later if needed
    }.get(command, lambda x: command)

    return typ(args)


if __name__ == "__main__":
    print(get_type('005'))