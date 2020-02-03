import Learner as learner
import Teacher as teacher
import sys

if __name__ == "__main__":
    t = teacher.Teacher()
    sys.stdout = open('test.html', 'w')

    # the teacher is showing the language of {a^n, b^m| n & m even}
    # for testing I used only two counter example: ["ab", "abab"]
    l = learner.Learner(t.teacher_method)

    # start learning.......
    l.learn(t.teacher_method, t.exs)



