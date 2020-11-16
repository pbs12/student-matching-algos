% runningAverageOverall = [];
% runningAverageMinorities = [];
% for i = 1:10
%     
%     
% end    

avgPercentageEachGenNoMR = [];
avgPercentageEachGenMR = [];

AA = readmatrix('minortyProp.csv');
for i = 2:2:20
   tempAvgNoMR = mean(AA(:,i),'all');
   avgPercentageEachGenNoMR = [avgPercentageEachGenNoMR; tempAvgNoMR]; 
end
for j = 3:2:21
   tempAvgMR = mean(AA(:,j),'all');
   avgPercentageEachGenMR = [avgPercentageEachGenMR; tempAvgMR]; 
end

figure(1)
X = categorical({'Without Minority Reserves','With Minority Reserves'});
X = reordercats(X,{'Without Minority Reserves','With Minority Reserves'});

bar(X,[mean(avgPercentageEachGenNoMR) mean(avgPercentageEachGenMR)])
title("Market Diversity of Deferred Acceptance with and without Affirmative Action");
ylabel("Average Percentage of Minorities at Each Company (%)")
xlabel("Algorithm Type")

BB = readmatrix('topChoiceOptimalityMinorities.csv');


BB2 = BB(:,1:10);
for i = 1:size(BB2,1)
    row = BB2(i,:);
    rowSum = sum(row,'all');
    BB2(i,:) = BB2(i,:)/rowSum;   
end
BB3 = [zeros(1,size(BB2,2)); zeros(1,size(BB2,2))];

poop = 1;
for j = 1:size(BB2,1)
   if mod(j,2) == 1
       BB3(1,:) = BB3(1,:)+BB2(j,:);
   end
   
   if mod(j,2) == 0
       BB3(2,:) = BB3(2,:)+BB2(j,:);
   end
end
BB3 = BB3./size(BB2,1)*2*100;

figure(2)
h = bar(BB3')
title({"Percentage of Students Matched with a Top 10 Pick", "through Deferred Acceptance with and without Affirmative Action"});
ylabel("Percentage of Minorities who recieved their nth pick(%)")
xlabel("n")
set(h, {'DisplayName'}, {'Without Minority Reserves','With Minority Reserves'}')
legend()