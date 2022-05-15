### MMAB Chess.py
- Chess library와 MMAB가 적용된 체스 프로그램
- AI가 white, 사용자가 black
- depth와 evaluate_board를 통해 다음 수를 두었을 때 보드 상태의 점수를 계산하여 다음 수를 선택하는 방식

-------------------------------------------------------------------------------------
### MCTS Chess.py
- Chess library와 MCTS가 적용된 체스 프로그램
- AI가 white(1), 사용자가 black(0)
- UCB가 적용되어 있음

-------------------------------------------------------------------------------------
### MCTS Chess without UCB.py
- 기존 MCTS Chess에서 UCB를 제거함
- child node를 선택하는 기준을 UCB에서 랜덤으로 변경

-------------------------------------------------------------------------------------
### To Do
- 알고리즘끼리 대결할 수 있도록 하기
- stalemate, insufficient material 기능 추가하기

-------------------------------------------------------------------------------------

#### Reference
##### python chess library
https://python-chess.readthedocs.io/en/latest/index.html
##### Monte Carlo Tree Search Application on Chess
https://medium.com/@ishaan.gupta0401/monte-carlo-tree-search-application-on-chess-5573fc0efb75
