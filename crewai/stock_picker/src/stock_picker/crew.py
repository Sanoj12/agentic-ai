from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from pydantic import BaseModel, Field
from crewai_tools import TavilySearchTool


##basemode subclass
class TrendingCompany(BaseModel):
    """A company that is in the news and attention"""
    name: str = Field(description="company name")
    ticker: str =Field(description="stock ticker symbol")
    reason: str = Field(description="Reason the trending in the news")

class TrendingCompanyList(BaseModel):
    """List of multiple trending companies that are in the news"""
    companies: List[TrendingCompany] = Field(description="List of companies trending in the news")


class TrendingCompanyResearch(BaseModel):
    """Detailed research on a company"""
    name: str = Field(description="company name")
    market_position:str = Field(description="current market position and analysis")
    future: str = Field(description="future outlook and growth prospects")
    investment : str= Field(description="investment pontenial")

class TrendingCompanyResearchList(BaseModel):
    """a list of detailed research on all the companies"""
    research_list: List[TrendingCompanyResearch] =Field(description="list of all researched list company")


@CrewBase
class StockPicker():
    """StockPicker crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    
    @agent
    def trading_company_finder(self) -> Agent:
        return Agent(
            config=self.agents_config['trading_company_finder'],
            tools=[TavilySearchTool()],
            use_fallback= False,
            verbose=True
           
            
        )

    @agent
    def finanical_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['finanical_researcher'], # type: ignore[index]
            tools=[TavilySearchTool()],
            use_fallback= False,
            verbose=True
        )

    
    @agent
    def stock_picker(self) -> Agent:
        return Agent(
            config=self.agents_config['stock_picker'], # type: ignore[index]
            tools=[TavilySearchTool()],
            use_fallback= False,
            verbose=True
     
        )


    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def finding_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['finding_trending_companies'], # type: ignore[index]
            output_pydantic=TrendingCompanyList
        )

    @task
    def research_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['research_trending_companies'], # type: ignore[index]
            output_pydantic=TrendingCompanyResearchList
        )
    
    @task
    def pick_best_company(self) -> Task:
        return Task(
            config=self.tasks_config['pick_best_company'], # type: ignore[index]
            
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the StockPicker crew"""
        manager = Agent(
            config=self.agents_config['manager'],
            allow_delegation=True
        )
      
        return Crew(
            agents = self.agents,
            tasks=self.tasks,
           process=Process.hierarchical,
            verbose =True, ##control the level of logging
            
            manager_agent = manager
        )