package org.srvvp.knowledgetree.entity;
// Generated 5 Apr, 2017 12:15:43 PM by Hibernate Tools 3.2.4.GA

import java.util.HashSet;
import java.util.Set;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.Id;
import javax.persistence.OneToMany;
import javax.persistence.Table;
import org.hibernate.validator.Length;
import org.hibernate.validator.NotNull;

/**
 * WorkWorkRelation generated by hbm2java
 */
@Entity
@Table(name = "work_work_relation", catalog = "knowledgetree")
public class WorkWorkRelation implements java.io.Serializable {

	private String id;
	private String name;
	private String description;
	private Set<WorkRelatestoWork> workRelatestoWorks = new HashSet<WorkRelatestoWork>(
			0);

	public WorkWorkRelation() {
	}

	public WorkWorkRelation(String id) {
		this.id = id;
	}
	public WorkWorkRelation(String id, String name, String description,
			Set<WorkRelatestoWork> workRelatestoWorks) {
		this.id = id;
		this.name = name;
		this.description = description;
		this.workRelatestoWorks = workRelatestoWorks;
	}

	@Id
	@Column(name = "id", unique = true, nullable = false, length = 20)
	@NotNull
	@Length(max = 20)
	public String getId() {
		return this.id;
	}

	public void setId(String id) {
		this.id = id;
	}

	@Column(name = "Name", length = 100)
	@Length(max = 100)
	public String getName() {
		return this.name;
	}

	public void setName(String name) {
		this.name = name;
	}

	@Column(name = "Description", length = 1000)
	@Length(max = 1000)
	public String getDescription() {
		return this.description;
	}

	public void setDescription(String description) {
		this.description = description;
	}

	@OneToMany(fetch = FetchType.LAZY, mappedBy = "workWorkRelation")
	public Set<WorkRelatestoWork> getWorkRelatestoWorks() {
		return this.workRelatestoWorks;
	}

	public void setWorkRelatestoWorks(Set<WorkRelatestoWork> workRelatestoWorks) {
		this.workRelatestoWorks = workRelatestoWorks;
	}

}