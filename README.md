### MCTS Chess.py
- MCTS가 White, MMAB가 Black
- UCB 적용 x
- 승점이 가장 높은 노드를 선택하도록

-------------------------------------------------------------------------------------
### MCTS with ucb.py
- MCTS가 White, MMAB가 Black
- UCB 적용 O

-------------------------------------------------------------------------------------
### MCTS with ucb and modified rollout.py
- MCTS가 White, MMAB가 Black
- UCB 적용 O
- rollout 단계에서 리프노드에 자식노드를 한번 더 expand하고 그 자식노드들에서 시뮬레이션을 거쳐 누적된 승점이 가장 높은 자식노드로 시뮬레이션을 진행하도록

-------------------------------------------------------------------------------------
### To Do
- Simulation Function 개선 마무리
- 승률은 최대, 시간은 최소화하는 최적의 반복수와 깊이 탐색

-------------------------------------------------------------------------------------

#### Reference
##### python chess library
https://python-chess.readthedocs.io/en/latest/index.html
##### Monte Carlo Tree Search Application on Chess
https://medium.com/@ishaan.gupta0401/monte-carlo-tree-search-application-on-chess-5573fc0efb75
##### Minimax Application on Chess
https://medium.com/dscvitpune/lets-create-a-chess-ai-8542a12afef
