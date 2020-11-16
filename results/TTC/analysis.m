% runningAverageOverall = [];
% runningAverageMinorities = [];
% for i = 1:10
%     
%     
% end    

avgPercentageEachGenNoMR = [];
avgPercentageEachGenMR = [];

A = readmatrix('minortyProp.csv');
for i = 2:2:20
   tempAvgNoMR = mean(A(:,i),'all');
   avgPercentageEachGenNoMR = [avgPercentageEachGenNoMR; tempAvgNoMR]; 
end
for j = 3:2:21
   tempAvgMR = mean(A(:,j),'all');
   avgPercentageEachGenMR = [avgPercentageEachGenMR; tempAvgMR]; 
end

figure(1)
X = categorical({'Without Minority Reserves','With Minority Reserves'});
X = reordercats(X,{'Without Minority Reserves','With Minority Reserves'});

bar(X,[mean(avgPercentageEachGenNoMR) mean(avgPercentageEachGenMR)])
title("Market Diversity of Top Trading Cycle with and without Affirmative Action");
ylabel("Average Percentage of Minorities at Each Company (%)")
xlabel("Algorithm Type")

B = readmatrix('topChoiceOptimality.csv');


B2 = B(:,1:10);
for i = 1:size(B2,1)
    row = B(i,:);
    rowSum = sum(row,'all');
    B2(i,:) = B2(i,:)./rowSum;   
end
B3 = [zeros(1,size(B2,2)); zeros(1,size(B2,2))];

poop = 1;
for j = 1:size(B2,1)
   if mod(j,2) == 1
       B3(1,:) = B3(1,:)+B2(j,:);
   end
   
   if mod(j,2) == 0
       B3(2,:) = B3(2,:)+B2(j,:);
   end
end
B3 = B3./size(B2,1)*2*100;

figure(2)
h = bar(B3')
title({"Percentage of Students Matched with a Top 10 Pick", "through Top Trading Cycle with and without Affirmative Action"});
ylabel("Percentage of Minorities who recieved their nth pick(%)")
xlabel("n")
set(h, {'DisplayName'}, {'Without Minority Reserves','With Minority Reserves'}')
legend()

% runningAverageOverall = [];
% runningAverageMinorities = [];
% for i = 1:10
%     
%     
% end    

avgPercentageEachGenNoMR = [];
avgPercentageEachGenMR = [];

AA = readmatrix('minortyPropDA.csv');
for i = 2:2:20
   tempAvgNoMR = mean(AA(:,i),'all');
   avgPercentageEachGenNoMR = [avgPercentageEachGenNoMR; tempAvgNoMR]; 
end
for j = 3:2:21
   tempAvgMR = mean(AA(:,j),'all');
   avgPercentageEachGenMR = [avgPercentageEachGenMR; tempAvgMR]; 
end

figure(3)
X = categorical({'Without Minority Reserves','With Minority Reserves'});
X = reordercats(X,{'Without Minority Reserves','With Minority Reserves'});

bar(X,[mean(avgPercentageEachGenNoMR) mean(avgPercentageEachGenMR)])
title("Market Diversity of Deferred Acceptance with and without Affirmative Action");
ylabel("Average Percentage of Minorities at Each Company (%)")
xlabel("Algorithm Type")

BB = readmatrix('topChoiceOptimalityDA.csv');


BB2 = BB(:,1:10);
for i = 1:size(BB2,1)
    row = BB(i,:);
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

figure(4)
h = bar(BB3')
title({"Percentage of Students Matched with a Top 10 Pick", "through Deferred Acceptance with and without Affirmative Action"});
ylabel("Percentage of Minorities who recieved their nth pick(%)")
xlabel("n")
set(h, {'DisplayName'}, {'Without Minority Reserves','With Minority Reserves'}')
legend()


figure(5)
C = [B3(2,:); BB3(2,:)]; 
hh = bar(C')
title({"Percentage of Students Matched with a Top 10 Pick", "through DA and TTC with Affirmative Action"});
ylabel("Percentage of Students who recieved their nth pick(%)")
xlabel("n")
set(hh, {'DisplayName'}, {'TTC','DA'}')
legend()

