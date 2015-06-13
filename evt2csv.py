import os


err = 0
# String of event file ; end index of previous event of 0 for first event ; state (T/F) for replace names with 'EVT_*'
def evt_extract(string, sr, rw):
    start = string.lower().find("event = {", sr)
    evt_body = ["", 0]
    part1 = ""
    part2 = ""
    if start == -1:
        return -1
    else:
        level = 1
        evt_id = ""
        evt_name = ""
        evt_desc = ""
        for i in range(start + 10, len(string)):
            if string[i] == "{":
                level += 1
            elif string[i] == "}":
                level -= 1
            if level == 0:  # if event ends
                evt_body = [string[start:i + 1:1], i + 1]
                part1 = string[0:start:1]
                part2 = string[i + 1:len(string):1]
                while part2.rfind("\n") == 0:
                    part2 = part2[0:len(part2) - 1:1]
                break
        """
        EVENT ID
        """
        s_id = evt_body[0].lower().find("id =")
        for i in range(s_id, s_id + 15):
            if evt_body[0][i] == "\n":
                evt_id = evt_body[0][s_id + 5:i:1]
                evt_id.replace(" ", "")
                evt_id = int(evt_id)
                break
        #print('Event', evt_id, "is", end=' ')
        """
        NAME
        """
        s_name = evt_body[0].lower().find("name =")
        a = 0
        st = 0
        for i in range(s_name, len(evt_body[0])):
            if evt_body[0][i] == "\"" and st == 0:
                st = 1
                a = i
            elif evt_body[0][i] == "\"" and st == 1:
                evt_name = [evt_body[0][a + 1:i:1], a, i]
                # if evt_name[0].find("AI_") != 0:
                #    return [evt_id, evt_name[0], '', 0, [], sr+1, string]
                if rw and evt_name[0].find("EVT_") != 0:
                    evt_body[0] = evt_body[0][0:a + 1:1] \
                                  + "EVT_" + str(evt_id) + "_NAME" \
                                  + evt_body[0][i:len(evt_body[0]):1]
                break
        """
        DESCRIPTION
        """
        s_desc = evt_body[0].lower().find("desc =")
        a = 0
        st = 0
        for i in range(s_desc, len(evt_body[0])):
            if evt_body[0][i] == "\"" and st == 0:
                st = 1
                a = i
            elif evt_body[0][i] == "\"" and st == 1:
                evt_desc = [evt_body[0][a + 1:i:1], a, i]
                if rw and evt_desc[0].find("EVT_") != 0:
                    evt_body[0] = evt_body[0][0:a + 1:1] + "EVT_" + str(evt_id) + "_DESC" + evt_body[0][
                                                                                            i:len(evt_body[0]):1]

                break
        """
        ACTIONS
        """
        act_count = evt_body[0].lower().count("action =") \
                    + evt_body[0].lower().count("action_a =") \
                    + evt_body[0].lower().count("action_b =") \
                    + evt_body[0].lower().count("action_c =") \
                    + evt_body[0].lower().count("action_d =") \
                    + evt_body[0].lower().count("action_e =") \
                    + evt_body[0].lower().count("action_f =") \
                    + evt_body[0].lower().count("action_g =")
        ast = 0
        evt_actnames = []
        s_acts = []
        # find all indexes of action's
        c = [0]
        s_actions = [9999]
        for j in range(act_count):
            if evt_body[0].lower().find("action =", ast) != -1:
                s_acts.append(evt_body[0].lower().find("action =", ast))
            if evt_body[0].lower().find("action_a =", ast) != -1:
                s_acts.append(evt_body[0].lower().find("action_a =", ast))
            if evt_body[0].lower().find("action_b =", ast) != -1:
                s_acts.append(evt_body[0].lower().find("action_b =", ast))
            if evt_body[0].lower().find("action_c =", ast) != -1:
                s_acts.append(evt_body[0].lower().find("action_c =", ast))
            if evt_body[0].lower().find("action_d =", ast) != -1:
                s_acts.append(evt_body[0].lower().find("action_d =", ast))
            if evt_body[0].lower().find("action_e =", ast) != -1:
                s_acts.append(evt_body[0].lower().find("action_e =", ast))
            if evt_body[0].lower().find("action_f =", ast) != -1:
                s_acts.append(evt_body[0].lower().find("action_f =", ast))
            if evt_body[0].lower().find("action_g =", ast) != -1:
                s_acts.append(evt_body[0].lower().find("action_g =", ast))
            c.append(len(s_acts))
            ast = min(s_acts[c[j]:c[j+1]])+1    # That thing (s_acts) used for: if order of "action =" is wrong
            s_act = ast-1                       # (but game parse it)
            s_actions.remove(s_actions[-1])
            s_actions.append(s_act)
            s_actions.append(len(string))
            if evt_body[0].lower().find("name =", s_act) != -1 \
                    and evt_body[0].lower().find("name =", s_act) < s_actions[j+1]:
                s_actname = evt_body[0].lower().find("name =", s_act)
                a = 0
                st = 0
                for i in range(s_actname, len(evt_body[0])):
                    if evt_body[0][i] == "\"" and st == 0:
                        st = 1
                        a = i
                    elif evt_body[0][i] == "\"" and st == 1:
                        evt_actnames.append(evt_body[0][a + 1:i:1])

                        if rw and evt_actnames[::-1][0].find("EVT_") != 0:
                            evt_body[0] = evt_body[0][0:a + 1:1] + "EVT_" + str(evt_id) + "_OPTION" \
                                          + {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G"}.get(j, "ERR") \
                                          + evt_body[0][i:len(evt_body[0]):1]
                        break
            else:
                # debug for ERR
                act_count -= 1
                # print(s_act, evt_body[0][s_act:len(evt_body[0]):1])
        """
        REPLACE SUB-STRING EVENT WITH NEW GENERATED EVENT
        """
        if rw:
            new_string = part1 + evt_body[0] + part2
        else:
            new_string = ""
        index = len(part1 + evt_body[0]) + 1
        return [evt_id, evt_name[0], evt_desc[0], act_count, evt_actnames, index, new_string]

dirs = os.listdir(os.getcwd())
for j in dirs:
    for i in j:
        if i == '.':
            dirs.remove(j)
for cur_dir in dirs:
    events = os.listdir(os.getcwd() + "\\" + cur_dir + "\\")
    str_csv = ""
    for cur_evt in events:
        print("\\"+cur_dir+"\\"+cur_evt)
        with open(os.getcwd() + "\\" + cur_dir + "\\" + cur_evt, mode='r') as f:
            file_str = f.read()
        # fix bad syntax
        file_str = file_str.replace("name=", "name =")
        file_str = file_str.replace("id=", "id =")
        file_str = file_str.replace("event=", "event =")
        file_str = file_str.replace("desc=", "desc =")
        file_str = file_str.replace("action=", "action =")
        file_str = file_str.replace("action_a=", "action_a =")
        file_str = file_str.replace("action_b=", "action_b =")
        file_str = file_str.replace("action_c=", "action_c =")
        file_str = file_str.replace("action_d=", "action_d =")
        file_str = file_str.replace("action_e=", "action_e =")
        file_str = file_str.replace("action_f=", "action_f =")
        file_str = file_str.replace("action_g=", "action_g =")

        buf = [0, 0, 0, 0, 0, 0]
        # extract all events
        while True:
            buf = evt_extract(file_str, buf[5], True)
            if buf == -1:
                break
            if buf[1].find("EVT_") != 0:
                str_csv += "EVT_" + str(buf[0]) + "_NAME;" + buf[1] + ";\n"
            if buf[2].find("EVT_") != 0:
                str_csv += "EVT_" + str(buf[0]) + "_DESC;" + buf[2] + ";\n"
            # if buf[3] == len(buf[4]):
                # print("OK")
            # else:
                # debug if count of actions != action names
                # print(":", buf[3], buf[4])
            if buf[3] != len(buf[4]):
                err +=1
            for i in range(buf[3]):
                if buf[4][i].find("EVT_") != 0:
                    str_csv += "EVT_" + str(buf[0]) + "_OPTION" \
                               + {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G"}.get(i, "ERR") \
                               + ";" + buf[4][i] + ";\n"
            file_str = buf[6]
        # write new file
        with open(os.getcwd() + "\\" + cur_dir + "\\" + cur_evt, mode='w') as f:
            f.write(file_str)

    with open(os.getcwd() + "\\" + cur_dir + ".csv", mode='w') as f:
        f.write(str_csv)

print("Errors: ", err)