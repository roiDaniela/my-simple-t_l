
import ObservationTable as table

class Learner:
    def __init__(self, t, a="ab"):
        self.alphabets = a
        self.status = "init"
        self.ObservationTable = table.ObservationTable(t)

    def learn(self, teacher, exs=[]):
        """
        """
        """
        THIS CODE SECTION IS FOR VIEW
        """
        print("<html>")
        self.ObservationTable.print_table(teacher)
        print("<hr/>")
        """ 
        """

        # loop till no counterexample
        while True:
            # check closed and consistent and update table
            self.update(teacher)

            """ 
            THIS CODE SECTION IS FOR VIEW
            """
            self.ObservationTable.print_table(teacher)
            print("status:%s" % self.status)
            print("<hr/>")
            """ 
            """

            # if closed and consistent ask teacher for counterexample
            if self.status == "ok":
                if len(exs) == 0:
                    break
                else:
                    # get counterexample
                    ex = exs.pop(0)

                    # update table with counterexample
                    self.ObservationTable.add_counterexample_to_table(teacher, ex)

                    """ 
                    THIS CODE SECTION IS FOR VIEW
                    """
                    print("<hr/>")
                    """ 
                    """
        """ 
        THIS CODE SECTION IS FOR VIEW
        """
        print("</html>")
        """ 
        """

    def update(self, teacher):
        # it's actually a hack to send string by ref (https://stackoverflow.com/questions/986006/how-do-i-pass-a-variable-by-reference)
        status_wrapper = [self.status]

        # check closed
        if not self.ObservationTable.check_close(teacher, status_wrapper): #if not closed return false
            self.status = status_wrapper[0]
            return False

        status_wrapper = [self.status]

        # closed
        # is consistent?
        if not self.ObservationTable.check_consistent(teacher, status_wrapper): #if not consistent return false
            self.status = status_wrapper[0]
            return False

        # closed and consistent
        self.status = "ok"
        return True