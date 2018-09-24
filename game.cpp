#include <iostream>
#include <map>
#include <string>

using namespace std;
map < int , map < int , map < string , int > > > grid;
map < int , map < int , string > > grid_occu_by;
map < int , string > player_nickname;

int no_cols, no_rows;
int no_players;
int active_players;

string default_player="n";

void print_grid()
{
    cout<<"r/c    ";
    for(int i=0;i<no_cols;i++)
    {
        cout<<"c-"<<i<<"  ";
    }
    cout<<endl<<endl;
    for(int i=0;i<no_rows;i++)
    {
        cout<<"r-"<<i<<"    ";
        for(int j=0;j<no_cols;j++)
        {
            cout<<grid_occu_by[i][j]<<"-"<<grid[i][j][grid_occu_by[i][j]]<<"  ";
        }
        cout<<endl;
    }
    cout<<endl;
}
int player_active_status(string name)
{
    for(int i=0;i<no_rows;i++)
    {
        for(int j=0;j<no_cols;j++)
        {
            if(grid_occu_by[i][j]==name)
            {
                return 1;
            }
        }
    }
    return 0;
}
void check_active_players()
{
    active_players=0;
    for(int i=0;i<no_players;i++)
    {
        active_players+=player_active_status(player_nickname[i]);
    }
}
void upgrade_grid(int x,int y,string name);
void mini_upgrade(int x,int y,string name)
{
    grid[x][y][grid_occu_by[x][y]]+=1;
    grid[x][y][name]=grid[x][y][grid_occu_by[x][y]];
    if(grid_occu_by[x][y]!=name)
    {
        grid[x][y][grid_occu_by[x][y]]=0;
        grid_occu_by[x][y]=name;
    }
    upgrade_grid(x,y,name);
}
void upgrade_grid(int x,int y,string name)
{
    check_active_players();
    if(active_players==1)
    {
        return;
    }
    if(x>0&&x<no_rows-1&&y>0&&y<no_cols-1)
    {
        if(grid[x][y][grid_occu_by[x][y]]==4)
        {
            grid[x][y][grid_occu_by[x][y]]=0;
            grid_occu_by[x][y]=default_player;
            mini_upgrade(x-1,y,name);
            mini_upgrade(x+1,y,name);
            mini_upgrade(x,y-1,name);
            mini_upgrade(x,y+1,name);

        }
        return;
    }
    if(x==0&&y>0&&y<no_cols-1)
    {
        if(grid[x][y][grid_occu_by[x][y]]==3)
        {
            grid[x][y][grid_occu_by[x][y]]=0;
            grid_occu_by[x][y]=default_player;
            mini_upgrade(x+1,y,name);
            mini_upgrade(x,y-1,name);
            mini_upgrade(x,y+1,name);
        }
        return;
    }
    if(x==no_rows-1&&y>0&&y<no_cols-1)
    {
        if(grid[x][y][grid_occu_by[x][y]]==3)
        {
            grid[x][y][grid_occu_by[x][y]]=0;
            grid_occu_by[x][y]=default_player;
            mini_upgrade(x-1,y,name);
            mini_upgrade(x,y-1,name);
            mini_upgrade(x,y+1,name);
        }
        return;
    }
    if(x>0&&x<no_rows-1&&y==0)
    {
        if(grid[x][y][grid_occu_by[x][y]]==3)
        {
            grid[x][y][grid_occu_by[x][y]]=0;
            grid_occu_by[x][y]=default_player;
            mini_upgrade(x-1,y,name);
            mini_upgrade(x+1,y,name);
            mini_upgrade(x,y+1,name);
        }
        return;
    }
    if(x>0&&x<no_rows-1&&y==no_cols-1)
    {
        if(grid[x][y][grid_occu_by[x][y]]==3)
        {
            grid[x][y][grid_occu_by[x][y]]=0;
            grid_occu_by[x][y]=default_player;
            mini_upgrade(x-1,y,name);
            mini_upgrade(x+1,y,name);
            mini_upgrade(x,y-1,name);
        }
        return;
    }
    if(x==0&&y==0)
    {
        if(grid[x][y][grid_occu_by[x][y]]==2)
        {
            grid[x][y][grid_occu_by[x][y]]=0;
            grid_occu_by[x][y]=default_player;
            mini_upgrade(x+1,y,name);
            mini_upgrade(x,y+1,name);
        }
        return;
    }
    if(x==0&&y==no_cols-1)
    {
        if(grid[x][y][grid_occu_by[x][y]]==2)
        {
            grid[x][y][grid_occu_by[x][y]]=0;
            grid_occu_by[x][y]=default_player;
            mini_upgrade(x+1,y,name);
            mini_upgrade(x,y-1,name);
        }
        return;
    }
    if(x==no_rows-1&&y==0)
    {
        if(grid[x][y][grid_occu_by[x][y]]==2)
        {
            grid[x][y][grid_occu_by[x][y]]=0;
            grid_occu_by[x][y]=default_player;
            mini_upgrade(x-1,y,name);
            mini_upgrade(x,y+1,name);
        }
        return;
    }
    if(x==no_rows-1&&y==no_cols-1)
    {
        if(grid[x][y][grid_occu_by[x][y]]==2)
        {
            grid[x][y][grid_occu_by[x][y]]=0;
            grid_occu_by[x][y]=default_player;
            mini_upgrade(x-1,y,name);
            mini_upgrade(x,y-1,name);
        }
        return;
    }
}

int main()
{
    cout << "enter number of players" << endl;
    cin>>no_players;
    cout<< " enter gid size"<<endl;
    cin>>no_cols>>no_rows;
    for(int j=0;j<no_rows;j++)
    {
        for(int k=0;k<no_cols;k++)
        {
            grid_occu_by[j][k]="n";
            grid[j][k][grid_occu_by[j][k]]=0;
        }
    }
    for(int i=0;i<no_players;i++)
    {
        cout<<"player "<<i<<" please enter your nickname.(single lower case letter except n,c,r)"<<endl;
        cin>>player_nickname[i];
        for(int j=0;j<no_rows;j++)
        {
            for(int k=0;k<no_cols;k++)
            {
                grid[j][k][player_nickname[i]]=0;
            }
        }
    }
    print_grid();
    for(int i=0;i<no_players;i++)
    {
        cout<<"player "<<player_nickname[i]<<" please enter the position where you want to place your point"<<endl;
        int x,y;
        cin>>x>>y;
        while((grid_occu_by[x][y]!="n")||(!(x>=0&&x<no_rows))||(!(y>=0&&y<no_cols)))
        {
            if((!(x>=0&&x<no_rows))||(!(y>=0&&y<no_cols)))
                cout<<"d0-the position that you've entered is outside the playing grid"<<endl;
            else
                cout<<"the position that you've entered is already occupied by player "<<grid_occu_by[x][y]<<". So please enter another position where you want place your point"<<endl;
            cin>>x>>y;
        }
        grid_occu_by[x][y]=player_nickname[i];
        grid[x][y][player_nickname[i]]+=1;
        print_grid();
    }
    check_active_players();
    while(active_players>1)
    {
        for(int i=0;i<no_players;i++)
        {
            if(player_active_status(player_nickname[i])==1)
            {
                cout<<"player "<<player_nickname[i]<<" please enter the position where you want to place your point"<<endl;
                int x,y;
                cin>>x>>y;
                while(((grid_occu_by[x][y]!="n")&&grid_occu_by[x][y]!=player_nickname[i])||(!(x>=0&&x<no_rows))||(!(y>=0&&y<no_cols)))
                {
                    if((!(x>=0&&x<no_rows))||(!(y>=0&&y<no_cols)))
                        cout<<"the position that you've entered is outside the playing grid"<<endl;
                    else
                        cout<<"the position that you've entered is already occupied by player "<<grid_occu_by[x][y]<<". So please enter another position where you want place your point"<<endl;
                    cin>>x>>y;
                }
                grid_occu_by[x][y]=player_nickname[i];
                grid[x][y][player_nickname[i]]+=1;
                upgrade_grid(x,y,player_nickname[i]);
                print_grid();
            }
        }
        check_active_players();
    }
    for(int i=0;i<no_players;i++)
    {
        if(player_active_status(player_nickname[i])==1)
        {
            cout<<"player "<<player_nickname[i]<<" won the game"<<endl;
        }
    }
    return 0;
}
