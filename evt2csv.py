def evt_extract(string, sr, rw):  # String of event file ; end index of previous event of 0 for first event ; state (T/F) for replace names with 'EVT_*'
    start = string.lower().find("event = {", sr)
    if start == -1:
        return -1
    else:
        level = 1
        evt_id = ""
        evt_name = ""
        evt_desc = ""
        for i in range(start + 10, len(string)):
            if string[i] == "{":
                level = level + 1
            elif string[i] == "}":
                level = level - 1
            if level == 0:  # if event ends
                evt_body = [string[start:i+1:1], i+1]
                part1 = string[0:start:1]
                part2 = string[i+1:len(string):1]
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
                if rw == True:
                    evt_body[0] = evt_body[0][0:a+1:1] + "EVT_" + str(evt_id) + "_NAME" + evt_body[0][i:len(evt_body[0]):1]
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
                if rw == True:
                    evt_body[0] = evt_body[0][0:a+1:1] + "EVT_" + str(evt_id) + "_DESC" + evt_body[0][i:len(evt_body[0]):1]

                break
        """
        ACTIONS
        """
        act_count = evt_body[0].lower().count("action =") + evt_body[0].lower().count("action_a =") \
                    + evt_body[0].lower().count("action_b =") + evt_body[0].lower().count("action_c =") \
                    + evt_body[0].lower().count("action_d =") + evt_body[0].lower().count("action_e =") \
                    + evt_body[0].lower().count("action_f =") + evt_body[0].lower().count("action_g =")
        ast = 0
        evt_actnames = []
        for j in range(act_count):
            s_act = [evt_body[0].lower().find("action =", ast), evt_body[0].lower().find("action_a =", ast), \
                     evt_body[0].lower().find("action_b =", ast), evt_body[0].lower().find("action_c =", ast), \
                     evt_body[0].lower().find("action_d =", ast), evt_body[0].lower().find("action_e =", ast), \
                     evt_body[0].lower().find("action_f =", ast), evt_body[0].lower().find("action_g =", ast)]

            for i in s_act:
                if i == -1:
                    s_act.remove(i)
            ast = s_act[0] + 5
            s_actname = evt_body[0].lower().find("name =", s_act[0])
            a = 0
            st = 0
            for i in range(s_actname, len(evt_body[0])):
                if evt_body[0][i] == "\"" and st == 0:
                    st = 1
                    a = i
                elif evt_body[0][i] == "\"" and st == 1:
                    evt_actnames.append(evt_body[0][a + 1:i:1])
                    if rw == True:
                        evt_body[0] = evt_body[0][0:a+1:1] + "EVT_" + str(evt_id) + "_OPTION" \
                                      + {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G"}.get(j, "ERR") \
                                      + evt_body[0][i:len(evt_body[0]):1]
                    break
        """
        REPLACING NAMES, DESC'S
        """
        if rw:
            new_string = part1 + evt_body[0] + part2
        else:
            new_string = ""
        if new_string.find(part2) == 0:
            index = sr+1
        else:
            index = new_string.find(part2)

        return [evt_id, evt_name[0], evt_desc[0], act_count, evt_actnames, index, new_string]


f = open('eventtest.txt')
file_str = f.read()
f.close()

buf = [0, 0, 0, 0, 0, 0]
str_csv = ""

while True:
    buf = evt_extract(file_str, buf[5], True)
    if buf == -1:
        break
    if buf[1].find("EVT_") != 0:
        str_csv += "EVT_" + str(buf[0]) + "_NAME;" + buf[1] + ";\n"
    if buf[2].find("EVT_") != 0:
        str_csv += "EVT_" + str(buf[0]) + "_DESC;" + buf[2] + ";\n"
    for i in range(buf[3]):
        if buf[4][i].find("EVT_") != 0:
            str_csv += "EVT_" + str(buf[0]) + "_OPTION" \
                    + {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G"}.get(i, "ERR") \
                    + ";" + buf[4][i] + ";\n"
    file_str = buf[6]


f = open("out.txt", mode='w')
f.write(file_str)
f.close()

f = open("out.csv", mode='w')
f.write(str_csv)
f.close()