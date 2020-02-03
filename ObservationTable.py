import graphviz
import sys

# Observation Table example:
#####################################
# S          #       e      #TRUE
#####################################
# S{a, b}    #       a      #FALSE
#                    b      #FALSE
#####################################
#
# Closure of Observation Table:
# An observation table is called closed provided that for each t in S.A there exist an s in S such that row(t) = row(s)
# Not Closed means:- There is a row(s1·a) in S.A is different from all s in S To resolve this add s1·a to S
#
# Consistency of Observation Table:-
# An observation table is called consistent provided that whenever s1 and s2 are elements of S such that row(s1) = row(s2) and for all a in A, row(s1·a) = ro(s2·a)
# Not Consistent means:-
# There exist a certain combination of s1 and s2 in S, e in E, and a in A such that row(s1) = row(s2) but T(s1·a·e)!=T(s2·a·e) To resolve this add a·e to E
#
# The set of strings S represents the states of the automaton constructed by the Learner.
# Entry (s, e) of the table represents the fact that from state s the
# automaton accepts/rejects the string s · e.
#
# in this class
# self.rows is S
# self.columns is E
# self.table is the automaton

class ObservationTable:
    def __init__(self, t, a="ab"):
        self.alphabets = a
        self.rows = [""]
        self.columns = [""]
        self.table = self.make_table(t, self.rows, self.columns)

    def check_consistent(self, teacher, status):
        '''
        :param teacher: oracle method to answer Membership queries
        :param status:update status for view
        :return: True if consistent and False if not
        '''

        # self.table is the states table, and table_trans is the input language option
        # get all possible options for rows (s1.a)
        # [s1 belongs to (S) self.rows and a belongs to alphabet (A)]
        rows_trans = self.make_rows_trans()
        # makes membership queries to obtain the table_trans:
        table_trans = self.make_table(teacher, rows_trans, self.columns)

        # closed
        # is consistent?
        # check if there exist a certain combination of s1 and s2 in self.rows (S), e in self.columns (E), and a in alphabet (A) such that row(s1) = row(s2) but T(s1·a·e)!=T(s2·a·e)
        for i in range(len(self.rows)):
            for j in range(i+1, len(self.rows)):
                #row(s1) = row(s2)
                if self.get_row(self.table, self.rows[i]) == self.get_row(self.table, self.rows[j]):
                    for a in self.alphabets:
                        # T(s1·a·e) != T(s2·a·e)
                        if self.get_row(table_trans, self.rows[i]+a) != self.get_row(table_trans, self.rows[j]+a):
                            #incosnsitent!
                            # To resolve this add a·e to self.columns (E)
                            newcol = [c+a for c in self.columns]
                            self.columns += newcol

                            # update table
                            self.table = self.make_table(teacher, self.rows, self.columns)
                            status[0] = "not consistent (%s, %s; %s)" % (self.rows[i], self.rows[j], a)
                            return False
        return True

    def check_close(self, teacher, status):
        '''
        :param teacher: oracle method to answer Membership queries
        :param status:update status for view
        :return: True if closed and False if not
        '''

        # self.table is the states table, and table_trans is the input language option
        # get all possible options for rows (s1.a)
        # [s1 belongs to (S) self.rows and a belongs to alphabet (A)]
        rows_trans = self.make_rows_trans()
        # makes membership queries to obtain the table_trans:
        table_trans = self.make_table(teacher, rows_trans, self.columns)

        # is closed?
        # not closed means that there is a row(s1·a) s1 belongs to self.rows (S) and a belongs to alphabet (A) in S.A
        # with different result from all results for T(s) in self.rows (S)
        for rt in rows_trans:
            found = False
            for r in self.rows:
                if self.get_row(table_trans, rt) == self.get_row(self.table, r):
                    found = True
                    break
            if not found:
                # not closed
                # To resolve this add s1·a to self.rows (S)
                self.rows.append(rt)

                # update table
                self.table = self.make_table(teacher, self.rows, self.columns)
                status[0] = "not closed (%s; %s)" % (r, rt)
                return False
        return True

    def make_table(self, ask_teacher_about_string, rows_= None, columns_ = None):
        if rows_ is None:
            rows_ = self.rows
        if columns_ is None:
            columns_ = self.columns

        t = {}
        for row in rows_:
            for col in columns_:
                # use Membership queries of the teacher to complete the table
                t[(row, col)] = ask_teacher_about_string(row + col)
        return t

    ''' HELPER FUNCTIONS'''
    # get entry r in table t
    def get_row(self, t, r):
        return [t[(r, c)] for c in self.columns]

    # get entry r in table t for view
    def get_row_as_str(self, t, r):
        return "".join(["1" if x else "0" for x in self.get_row(t, r)])
    '''END HELPER FUNCTIONS'''

    # calculate all concats of S{a,b}
    # self.rows + alphabet
    def make_rows_trans(self):
        rows_trans = []
        for r in self.rows:
            for a in self.alphabets:
                rows_trans.append(r + a)
        return rows_trans

    def print_table(self, teacher):
        rows_trans = []
        for r in self.rows:
            for a in self.alphabets:
                rows_trans.append(r + a)
        table_trans = self.make_table(teacher, rows_trans, self.columns)

        def f(x):
            if x == "":
                return "[]"
            else:
                return x

        print("<table rules=groups>")
        print("<colgroup/>")
        print("<thead>")
        print("<tr>")
        print("<td>*</td>")
        for c in self.columns:
            print("<td>%s</td>" % f(c))
        print("</tr>")
        print("</thead>")
        print("<tbody>")
        for r in self.rows:
            print("<tr>")
            print("<td>%s</td>" % f(r))
            for c in self.columns:
                print("<td>%s</td>" % self.table[(r, c)])
            print("</tr>")
        print("</tbody>")
        print("<tbody>")
        for r in rows_trans:
            print("<tr>")
            print("<td>%s</td>" % f(r))
            for c in self.columns:
                print("<td>%s</td>" % table_trans[(r, c)])
            print("</tr>")
        print("</tbody>")
        print("</table>")

    def draw(self, teacher):
        d = graphviz.Digraph()
        starting = [self.get_row_as_str(self.table, "")]
        accepting = []
        for i in self.rows:
            if self.table[(i, "")]:
                accepting.append(self.get_row_as_str(self.table, i))

        def f(s):
            ss = s
            if s in starting:
                ss += "S"
            if s in accepting:
                ss += "A"
            return ss

        for i in self.rows:
            d.node(f(self.get_row_as_str(self.table, i)))
        done = set()
        for i in self.rows:
            src_str = f(self.get_row_as_str(self.table, i))
            rows_trans = self.make_rows_trans()
            next_table = self.make_table(teacher, rows_trans, self.columns)
            for a in self.alphabets:
                dest = i + a
                dest_str = f(self.get_row_as_str(next_table, dest))
                if (src_str, dest_str, a) in done:
                    continue
                d.edge(src_str, dest_str, a)
                done.add((src_str, dest_str, a))
                # print("hoge")
        return d

    # Learner adds ex and its prefixes to his set self.rows (S)
    def add_counterexample_to_table(self, teacher, ex):
        for i in range(len(ex)):
            prefix = ex[:i]
            if self.rows.count(prefix) == 0:
                print("<p>Adding %s into the table.</p>" % prefix)
                self.rows.append(prefix)
            # update table
            self.table = self.make_table(teacher)