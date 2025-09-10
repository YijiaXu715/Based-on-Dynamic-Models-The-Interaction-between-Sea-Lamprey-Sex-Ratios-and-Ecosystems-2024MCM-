function Rc = calculate_reproduction_condition(agent, sexratio)
    % Initialize the Rc
    Rc = 1.0;
    % Age
    mature_age = 3; % 假设性成熟年龄为3
    if agent.age > mature_age
        Rc = Rc * 1.0;
    else
        Rc = Rc * 0.0; % 未成熟个体得分为0
    end    
    % Sex ratio
    if sexratio >= 1
        Rc = Rc * sexratio;
    else
        Rc = Rc * (2-sexratio); 
    end
end


