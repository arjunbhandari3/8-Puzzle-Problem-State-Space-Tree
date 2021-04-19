import sys
import os
import pydot

class State(object):
	Goal_State = [1, 2, 3, 8, 0, 4, 7,6,5]
	def __init__(self, State, parent, depthlimit, operation):
		self.State = State
		self.operation = operation 
		self.parent = parent
		self.depthlimit = depthlimit

	def Operations_Available(self, index):
		AvailableOperation = ['Down','Up','Right','Left']
		if (index == 0 or index == 3 or index == 6):
			AvailableOperation.remove('Left')

		if (index == 2 or index == 5 or index == 8):
			AvailableOperation.remove('Right')

		if (index == 0 or index == 1 or index == 2):
			AvailableOperation.remove('Up')

		if (index == 6 or index == 7 or index == 8):
			AvailableOperation.remove('Down')
		return AvailableOperation

	def curren_state(self):
		return self.State

	def current_state(self):
		print("|", end="")
		for i in range (0,3):
			print(str(self.State[i]) + "|", end="")
		print("\n")
		print("|", end="")
		for j in range(3,6):
			print(str(self.State[j]) + "|", end="")
		print("\n")
		print("|", end="")
		for k in range(6,9):
			print(str(self.State[k]) + "|", end="")
		print("\n" * 2)	

	def pattern_state(self):
		

		pattern= '''\ | {a} | {b} | {c} |\ \n | {d} | {e} | {f} |\ \n | {g} | {h} | {i} |\ \n
				\
				'''.format(a=self.State[0],b=self.State[1],c=self.State[2],d=self.State[3],e=self.State[4],f=self.State[5],g=self.State[6],h=self.State[7],i=self.State[8])
		return pattern

	def goal_state(self):
		if self.State == self.Goal_State:
			return True
		else:
			return False
		

	def next_state(self, current_state, depthlimit):
		#print(current_state.State)
		CurrentStateOriginal = current_state.State

		ListOfLegalOperation = list()
		ChildrenStates = list()
		index = current_state.State.index(0)
		ListOfLegalOperation = self.Operations_Available(index)
		print(ListOfLegalOperation[::-1])
		print("Depth", depthlimit)
		for operation in ListOfLegalOperation:
			if operation == 'Left':
				CurrentStateCopy = CurrentStateOriginal.copy()
				CurrentStateCopy[index], CurrentStateCopy[index - 1] = CurrentStateCopy[index - 1], CurrentStateCopy[index]
				NewState = State(CurrentStateCopy, current_state, depthlimit, 'Left')
				ChildrenStates.append(NewState)

			if operation == 'Right':
				CurrentStateCopy = CurrentStateOriginal.copy()
				CurrentStateCopy[index], CurrentStateCopy[index + 1] = CurrentStateCopy[index + 1], CurrentStateCopy[index]
				NewState = State(CurrentStateCopy, current_state, depthlimit, 'Right')
				ChildrenStates.append(NewState)

			if operation == 'Up':
				CurrentStateCopy = CurrentStateOriginal.copy()
				CurrentStateCopy[index], CurrentStateCopy[index - 3] = CurrentStateCopy[index - 3], CurrentStateCopy[index]
				NewState = State(CurrentStateCopy, current_state, depthlimit, 'Up')
				ChildrenStates.append(NewState)


			if operation == 'Down':
				CurrentStateCopy = CurrentStateOriginal.copy()
				CurrentStateCopy[index], CurrentStateCopy[index + 3] = CurrentStateCopy[index + 3], CurrentStateCopy[index]
				NewState = State(CurrentStateCopy, current_state, depthlimit, 'Down')
				ChildrenStates.append(NewState)
		return ChildrenStates
		



class Main(object):
	"""docstring for Main"""
	def __init__(self):
		states=[2,8,3,1,6,4,7,0,5]
		self.InitialState = State(states, None, 0, None)
		ChildrenStates = list()
		self.G = pydot.Dot(graph_type="digraph")
		node = pydot.Node(self.InitialState.pattern_state(),style = 'filled', fillcolor='green')
		self.G.add_node(node)

	def Depth_First_Search(self):
		if self.InitialState.goal_state():
			return self.InitialState
		Stacks = list()
		VisitedState = list()
		Stacks.insert(0, self.InitialState)
		nodes = self.InitialState.current_state()
		node = pydot.Node(self.InitialState.pattern_state(),style = 'filled', fillcolor='yellow')
		self.G.add_node(node)
		while Stacks:
			CurrentState = Stacks.pop(0)
			#MAKING TREE
			if CurrentState.parent!=None:
				node=pydot.Node(CurrentState.pattern_state(), style = 'filled', fillcolor='green')
				self.G.add_node(node)
				edge=pydot.Edge(CurrentState.parent.pattern_state(),CurrentState.pattern_state(), label=CurrentState.operation)
				self.G.add_edge(edge)	
			print("Current State : ")
			CurrentState.current_state()
			depthlimit = CurrentState.depthlimit
			print("DEPTHLIMIT: ", depthlimit)
			print("Goal State : ", CurrentState.goal_state())
			if CurrentState.goal_state():
				node=pydot.Node(CurrentState.pattern_state(), style = 'filled', fillcolor='pink')
				self.G.add_node(node)
				return CurrentState
			VisitedState.insert(0, CurrentState)
			if CurrentState.depthlimit < 5:

				ChildrenStates = CurrentState.next_state(CurrentState, depthlimit + 1)
				#print(len(ChildrenStates))
				
				for child in ChildrenStates:

					#print(VisitedState[0].current_state())\
					count=0
					for EachVisitedState in VisitedState:
						if (child.State == EachVisitedState.State):
							count=count + 1
					for EachStateInStacks in Stacks:
						if (child.State == EachStateInStacks.State):
							count = count + 1
					if count==0:
						Stacks.insert(0,child)
			
				#TEST STACKS AND Visited State
			print("STACKS")
			a=len(Stacks)
			for i in range(0,a):
				Stacks[i].current_state()
			print("VisitedState")
			b=len(VisitedState)
			for j in range(0,b):
				VisitedState[j].current_state()

		return "No SOLUTION" 
	def LegendGenerate(self):

		node=pydot.Node("State Space Tree of 8 Puzzle Problem in DEPTH WISE SEARCH", shape='none', fillcolor='yellow', fontsize='20')
		self.G.add_node(node)

		node1=pydot.Node("LEGEND", shape='none', fillcolor='yellow', fontsize='20')
		self.G.add_node(node1)

		Assignmentnode= pydot.Node("Arjun Bhandari (08) \n CE 4th Year",fontsize="30", fontcolor="black",  shape="none")
		self.G.add_node(Assignmentnode)

		edge=pydot.Edge(node,node1,style='invis')
		self.G.add_edge(edge)

		nodestart=pydot.Node("     ", shape='none', fillcolor='yellow', fontsize='20')
		self.G.add_node(nodestart)
		InitialStateNode=pydot.Node("Initial State",style='filled', fillcolor='yellow')
		self.G.add_node(InitialStateNode)

		patternode=pydot.Node("SOLUTION PATTERN = (Left, Right, Up, Down)", shape='none',fontsize='20')
		self.G.add_node(patternode)
		self.G.add_edge(pydot.Edge(InitialStateNode,patternode,style='invis'))
		self.G.add_edge(pydot.Edge(patternode,Assignmentnode,style='invis'))
		

		edge=pydot.Edge(nodestart,InitialStateNode,style='invis')
		self.G.add_edge(edge)

		GoalStateNode=pydot.Node("Goal State",style='filled', fillcolor='Pink')
		self.G.add_node(GoalStateNode)
		edge=pydot.Edge(nodestart,GoalStateNode,style='invis')
		self.G.add_edge(edge)


		ExploringNode=pydot.Node("Exploring Node",style='filled', fillcolor='green')
		self.G.add_node(ExploringNode)
		edge=pydot.Edge(nodestart,ExploringNode,style='invis')
		self.G.add_edge(edge)
		
obj= Main()

obj.Depth_First_Search()
obj.LegendGenerate()
obj.G.write_png('solution.png')
