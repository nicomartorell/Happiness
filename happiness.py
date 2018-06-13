import numpy as np
import matplotlib.pyplot as plt

#por ahora defino categorías (cats) como una lista de objetos Cat

total_time = 1000
look_back_time = 200

pos_event = 1
neg_event = -1

decay_constant = 0.05



class Cat:
    
    j = 0
    
    def __init__(self, state=0, availability=1, y_max=10, y_min=-10, p_pos_event=0.27, p_neg_event=0.27):
        self.id = Cat.j
        Cat.j+=1
        
        self.current_state = state
        self.d = availability
        self.y_max = y_max
        self.y_min = y_min
        self.p_pos = p_pos_event
        self.p_neg = p_neg_event
        
        self.y_list = np.zeros((total_time - look_back_time, 1))
    
    def generate_input(self, length):
        fn = np.zeros((length, 1))
        for i in range(length):
            r = np.random.rand()
            if(r < self.p_pos):
                fn[i] = pos_event
            elif(r < self.p_pos + self.p_neg):
                fn[i] = neg_event
        self.inp = fn
    
    def y(self, t):
        if(t<look_back_time):
            return
        
        result = 0
        for i in range(look_back_time):
            input_value = self.inp[t - i]
            input_mod = input_value * self.d
            filtered = input_mod * np.exp(-i*decay_constant)
            result += filtered
        
        if result > self.y_max:
            result = self.y_max
        elif result < self.y_min:
            result = self.y_min
        
        self.current_state = result
        return result    
    
    def calc_d(self):
        if(self.id == 0):
            return self.d
        
        prev_cat = cats[self.id - 1]
        self.d = ((prev_cat.current_state - prev_cat.y_min)/(prev_cat.y_max - prev_cat.y_min))



cats = [Cat(p_pos_event=0.6, p_neg_event=0), Cat(), Cat(), Cat(), Cat()]
h = np.zeros((total_time - look_back_time, 1))

for cat in cats:
    cat.generate_input(total_time)

for t in range(total_time - look_back_time):
    partial_sum = 0
    
    for cat in cats:
        cat.calc_d()
        cat.y_list[t] = cat.y(look_back_time + t)
        partial_sum += cat.y_list[t]
    
    h[t] = partial_sum/len(cats)

fig, ax = plt.subplots()
ax.plot(range(len(h)), h)
ax.set(xlabel="time", ylabel="h", title="h test medium life")
fig.savefig("h_test_medium_life.png")
plt.show()

"""
show input plot:

fig, ax = plt.subplots()
ax.plot(range(total_time), cats[0].inp)
ax.set(xlabel="time", ylabel="input", title="Input test")
fig.savefig("input_test.png")
plt.show()
"""