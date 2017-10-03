package org.srvvp.knowledgetree.entity;
// Generated 3 Oct, 2017 8:09:20 PM by Hibernate Tools 3.2.4.GA

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
 * Affiliation generated by hbm2java
 */
@Entity
@Table(name = "affiliation", catalog = "knowledgetree")
public class Affiliation implements java.io.Serializable {

	private String id;
	private String name;
	private Set<PersonHasAffiliation> personHasAffiliations = new HashSet<PersonHasAffiliation>(
			0);

	public Affiliation() {
	}

	public Affiliation(String id) {
		this.id = id;
	}
	public Affiliation(String id, String name,
			Set<PersonHasAffiliation> personHasAffiliations) {
		this.id = id;
		this.name = name;
		this.personHasAffiliations = personHasAffiliations;
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

	@OneToMany(fetch = FetchType.LAZY, mappedBy = "affiliation")
	public Set<PersonHasAffiliation> getPersonHasAffiliations() {
		return this.personHasAffiliations;
	}

	public void setPersonHasAffiliations(
			Set<PersonHasAffiliation> personHasAffiliations) {
		this.personHasAffiliations = personHasAffiliations;
	}

}