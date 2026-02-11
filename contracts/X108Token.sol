// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title X108Token
 * @dev Token utilitaire pour la gouvernance du Safety Gate X-108
 * 
 * "An agent should not pay because it can — it should pay only when the action survives time."
 * 
 * Ce token permet :
 * - Staking pour participer à la gouvernance
 * - Distribution de frais de transaction (0.1%) aux stakers
 * - Vote pour ajuster les paramètres de sécurité (temporal window, coherence threshold)
 */
contract X108Token {
    string public constant name = "X-108 Safety Token";
    string public constant symbol = "X108";
    uint8 public constant decimals = 18;
    uint256 public totalSupply;
    
    // Mapping des balances
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    
    // Staking
    mapping(address => uint256) public stakedBalance;
    mapping(address => uint256) public stakingTimestamp;
    uint256 public totalStaked;
    
    // Frais de transaction (0.1% = 10 basis points)
    uint256 public constant TRANSACTION_FEE_BPS = 10; // 0.1%
    uint256 public feePool; // Pool de frais à distribuer
    
    // Paramètres gouvernables du Safety Gate
    uint256 public temporalWindow = 10; // secondes
    uint256 public coherenceThreshold = 60; // 0.6 * 100 pour éviter les décimales
    
    // Gouvernance
    uint256 public proposalCount;
    mapping(uint256 => Proposal) public proposals;
    
    struct Proposal {
        uint256 id;
        address proposer;
        uint256 newTemporalWindow;
        uint256 newCoherenceThreshold;
        uint256 votesFor;
        uint256 votesAgainst;
        uint256 deadline;
        bool executed;
        mapping(address => bool) hasVoted;
    }
    
    // Events
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event Staked(address indexed user, uint256 amount);
    event Unstaked(address indexed user, uint256 amount);
    event RewardsClaimed(address indexed user, uint256 amount);
    event ProposalCreated(uint256 indexed proposalId, uint256 newTemporalWindow, uint256 newCoherenceThreshold);
    event Voted(uint256 indexed proposalId, address indexed voter, bool support, uint256 weight);
    event ProposalExecuted(uint256 indexed proposalId);
    event FeeCollected(uint256 amount);
    
    constructor(uint256 _initialSupply) {
        totalSupply = _initialSupply * 10**decimals;
        balanceOf[msg.sender] = totalSupply;
        emit Transfer(address(0), msg.sender, totalSupply);
    }
    
    /**
     * @dev Transfer tokens
     */
    function transfer(address _to, uint256 _value) public returns (bool success) {
        require(balanceOf[msg.sender] >= _value, "Insufficient balance");
        require(_to != address(0), "Invalid address");
        
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        
        emit Transfer(msg.sender, _to, _value);
        return true;
    }
    
    /**
     * @dev Approve spender
     */
    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }
    
    /**
     * @dev Transfer from
     */
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        require(_value <= balanceOf[_from], "Insufficient balance");
        require(_value <= allowance[_from][msg.sender], "Insufficient allowance");
        require(_to != address(0), "Invalid address");
        
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        allowance[_from][msg.sender] -= _value;
        
        emit Transfer(_from, _to, _value);
        return true;
    }
    
    /**
     * @dev Stake tokens pour participer à la gouvernance
     */
    function stake(uint256 _amount) public {
        require(balanceOf[msg.sender] >= _amount, "Insufficient balance");
        require(_amount > 0, "Amount must be > 0");
        
        balanceOf[msg.sender] -= _amount;
        stakedBalance[msg.sender] += _amount;
        stakingTimestamp[msg.sender] = block.timestamp;
        totalStaked += _amount;
        
        emit Staked(msg.sender, _amount);
    }
    
    /**
     * @dev Unstake tokens
     */
    function unstake(uint256 _amount) public {
        require(stakedBalance[msg.sender] >= _amount, "Insufficient staked balance");
        require(_amount > 0, "Amount must be > 0");
        
        stakedBalance[msg.sender] -= _amount;
        balanceOf[msg.sender] += _amount;
        totalStaked -= _amount;
        
        emit Unstaked(msg.sender, _amount);
    }
    
    /**
     * @dev Collecter les frais de transaction (appelé par le backend)
     */
    function collectFee(uint256 _transactionAmount) public returns (uint256 fee) {
        fee = (_transactionAmount * TRANSACTION_FEE_BPS) / 10000;
        feePool += fee;
        
        emit FeeCollected(fee);
        return fee;
    }
    
    /**
     * @dev Calculer les récompenses d'un staker
     */
    function calculateRewards(address _staker) public view returns (uint256) {
        if (totalStaked == 0) return 0;
        
        uint256 stakerShare = (stakedBalance[_staker] * 10000) / totalStaked;
        uint256 rewards = (feePool * stakerShare) / 10000;
        
        return rewards;
    }
    
    /**
     * @dev Claim rewards from fee pool
     */
    function claimRewards() public {
        uint256 rewards = calculateRewards(msg.sender);
        require(rewards > 0, "No rewards to claim");
        require(feePool >= rewards, "Insufficient fee pool");
        
        feePool -= rewards;
        balanceOf[msg.sender] += rewards;
        
        emit RewardsClaimed(msg.sender, rewards);
    }
    
    /**
     * @dev Créer une proposition de gouvernance
     */
    function createProposal(uint256 _newTemporalWindow, uint256 _newCoherenceThreshold) public returns (uint256) {
        require(stakedBalance[msg.sender] > 0, "Must stake to propose");
        require(_newTemporalWindow >= 5 && _newTemporalWindow <= 30, "Temporal window must be 5-30s");
        require(_newCoherenceThreshold >= 30 && _newCoherenceThreshold <= 90, "Coherence must be 0.3-0.9");
        
        proposalCount++;
        Proposal storage proposal = proposals[proposalCount];
        proposal.id = proposalCount;
        proposal.proposer = msg.sender;
        proposal.newTemporalWindow = _newTemporalWindow;
        proposal.newCoherenceThreshold = _newCoherenceThreshold;
        proposal.deadline = block.timestamp + 7 days;
        proposal.executed = false;
        
        emit ProposalCreated(proposalCount, _newTemporalWindow, _newCoherenceThreshold);
        return proposalCount;
    }
    
    /**
     * @dev Voter sur une proposition
     */
    function vote(uint256 _proposalId, bool _support) public {
        require(stakedBalance[msg.sender] > 0, "Must stake to vote");
        Proposal storage proposal = proposals[_proposalId];
        require(block.timestamp < proposal.deadline, "Voting period ended");
        require(!proposal.hasVoted[msg.sender], "Already voted");
        
        uint256 weight = stakedBalance[msg.sender];
        proposal.hasVoted[msg.sender] = true;
        
        if (_support) {
            proposal.votesFor += weight;
        } else {
            proposal.votesAgainst += weight;
        }
        
        emit Voted(_proposalId, msg.sender, _support, weight);
    }
    
    /**
     * @dev Exécuter une proposition si elle est approuvée
     */
    function executeProposal(uint256 _proposalId) public {
        Proposal storage proposal = proposals[_proposalId];
        require(block.timestamp >= proposal.deadline, "Voting period not ended");
        require(!proposal.executed, "Already executed");
        require(proposal.votesFor > proposal.votesAgainst, "Proposal rejected");
        
        temporalWindow = proposal.newTemporalWindow;
        coherenceThreshold = proposal.newCoherenceThreshold;
        proposal.executed = true;
        
        emit ProposalExecuted(_proposalId);
    }
    
    /**
     * @dev Obtenir les paramètres actuels du Safety Gate
     */
    function getSafetyParameters() public view returns (uint256, uint256) {
        return (temporalWindow, coherenceThreshold);
    }
    
    /**
     * @dev Calculer l'APY pour les stakers (estimation basée sur le fee pool)
     */
    function estimateAPY() public view returns (uint256) {
        if (totalStaked == 0) return 0;
        
        // APY estimé = (feePool annuel / totalStaked) * 100
        // Simplifié pour la démo
        uint256 annualFees = feePool * 365; // Estimation simplifiée
        uint256 apy = (annualFees * 100) / totalStaked;
        
        return apy;
    }
}
